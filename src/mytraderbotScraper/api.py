# src/mytraderbotScraper/api.py
import polars as pl
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals

from mytraderbotScraper.spiders.boursorama_news import BoursoramaNewsSpider


def clean_df(df: pl.DataFrame) -> pl.DataFrame:
    delete_article = (
        "((Traduction automatisée par Reuters à l'aide de l'apprentissage\n"
        "automatique et de l'IA générative, veuillez vous référer à\n"
        "l'avertissement suivant: https://bit.ly/rtrsauto))"
    )

    return (
        df.drop("heure_liste", strict=False)
        # découper date
        .with_columns(df["date"].str.split(" à ").alias("date_split"))
        .with_columns([
            pl.col("date_split").list.get(0).alias("Date"),
            pl.col("date_split").list.get(1).alias("heures"),
        ])
        .drop(["date_split", "date"])
        # nettoyer article (suppression traduction Reuters + trim)
        .with_columns(
            df["article"]
            .str.replace(delete_article, "", literal=True)
            .str.strip_chars()
            .alias("article")
        )
        # supprimer bloc entre () seulement s'il est au tout début
        .with_columns(
            pl.col("article")
            .str.replace(r"^\([^)]*\)\s*", "", literal=False)
            .alias("article")
        )
        # split sur " - "
        .with_columns(pl.col("article").str.split(" - ").alias("article_split"))
        .with_columns(
            pl.when(pl.col("article_split").list.len() > 1)
              .then(pl.col("article_split").list.slice(1).list.join(" - "))
              .otherwise(pl.col("article"))
              .alias("article")
        )
        .drop("article_split")
    )



def fetch_boursorama_articles(pages: int = 1, clean: bool = True) -> pl.DataFrame:
    items = []

    def _on_item_scraped(item, response, spider):
        items.append(dict(item))

    settings = get_project_settings()
    BoursoramaNewsSpider.total_pages = pages

    process = CrawlerProcess(settings)
    crawler = process.create_crawler(BoursoramaNewsSpider)
    crawler.signals.connect(_on_item_scraped, signal=signals.item_scraped)

    process.crawl(crawler)
    process.start()

    df = pl.DataFrame(items)
    return clean_df(df) if clean else df


# src/mytraderbotScraper/api.py
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from mytraderbotScraper.spiders.boursorama_news import BoursoramaNewsSpider
from mytraderbotScraper.pipelines import CollectorPipeline


def fetch_boursorama_articles(pages: int = 1) -> pd.DataFrame:
    """
    Scrape articles from Boursorama and return a pandas DataFrame.

    Parameters
    ----------
    pages : int, optional (default=1)
        Number of pages to scrape (each page contains ~20 articles).

    Returns
    -------
    pd.DataFrame
        A DataFrame with columns: ["heure", "titre", "lien", "source", "article"].
    """

    # reset collected items for each run
    CollectorPipeline.collected_items = []

    settings = get_project_settings()
    settings.set("ITEM_PIPELINES", {"mytraderbotScraper.pipelines.CollectorPipeline": 100})

    process = CrawlerProcess(settings)

    BoursoramaNewsSpider.total_pages = pages
    process.crawl(BoursoramaNewsSpider)
    process.start()

    return pd.DataFrame(CollectorPipeline.collected_items)

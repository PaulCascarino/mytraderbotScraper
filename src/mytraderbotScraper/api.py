import pandas as pd
import asyncio

from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from mytraderbotScraper.spiders.boursorama_news import BoursoramaNewsSpider
from mytraderbotScraper.pipelines import CollectorPipeline
from twisted.internet import defer


def fetch_boursorama_articles(pages: int = 1) -> pd.DataFrame:
    """
    Scrape articles from Boursorama and return a pandas DataFrame.
    Works both in .py scripts and Jupyter notebooks.
    """
    # reset
    CollectorPipeline.collected_items = []

    settings = get_project_settings()
    settings.set(
        "ITEM_PIPELINES",
        {"mytraderbotScraper.pipelines.CollectorPipeline": 100},
    )

    BoursoramaNewsSpider.total_pages = pages

    try:
        asyncio.get_running_loop()
        in_notebook = True
    except RuntimeError:
        in_notebook = False

    if in_notebook:
        # 🔹 Mode Jupyter
        runner = CrawlerRunner(settings)

        async def crawl():
            await defer.ensureDeferred(runner.crawl(BoursoramaNewsSpider))

        import nest_asyncio
        nest_asyncio.apply()

        # Ici on utilise asyncio.run directement au lieu de run_until_complete
        asyncio.run(crawl())
    else:
        # 🔹 Mode script normal
        process = CrawlerProcess(settings)
        process.crawl(BoursoramaNewsSpider)
        process.start()

    return pd.DataFrame(CollectorPipeline.collected_items)

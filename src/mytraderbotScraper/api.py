import pandas as pd
import asyncio

from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from mytraderbotScraper.spiders.boursorama_news import BoursoramaNewsSpider
from mytraderbotScraper.pipelines import CollectorPipeline
from twisted.internet import asyncioreactor

# ensure AsyncioSelectorReactor is installed (safe to call multiple times)
try:
    asyncioreactor.install()
except Exception:
    pass


def fetch_boursorama_articles(pages: int = 1) -> pd.DataFrame:
    """
    Scrape articles from Boursorama and return a pandas DataFrame.
    Works both in .py scripts and Jupyter notebooks.
    """
    CollectorPipeline.collected_items = []

    settings = get_project_settings()
    settings.set(
        "ITEM_PIPELINES",
        {"mytraderbotScraper.pipelines.CollectorPipeline": 100},
    )

    BoursoramaNewsSpider.total_pages = pages

    try:
        # 🔹 Case 1: no loop running (normal .py script)
        loop = asyncio.get_running_loop()
        in_notebook = True
    except RuntimeError:
        # 🔹 Case 2: no running loop (script mode)
        in_notebook = False

    if in_notebook:
        # Run inside existing asyncio loop (Jupyter)
        runner = CrawlerRunner(settings)
        task = runner.crawl(BoursoramaNewsSpider)

        # Use nest_asyncio to allow nested event loops
        import nest_asyncio

        nest_asyncio.apply()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(task)
    else:
        # Normal Python script: safe to use CrawlerProcess
        process = CrawlerProcess(settings)
        process.crawl(BoursoramaNewsSpider)
        process.start()

    return pd.DataFrame(CollectorPipeline.collected_items)

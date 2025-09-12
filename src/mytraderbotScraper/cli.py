import scrapy
from scrapy.crawler import CrawlerProcess
from mytraderbotScraper.spiders.boursorama_news import BoursoramaNewsSpider


def run():
    process = CrawlerProcess(settings={
        "FEED_FORMAT": "json",
        "FEED_URI": "titres.json",
        "FEED_EXPORT_ENCODING": "utf-8",
    })
    process.crawl(BoursoramaNewsSpider)
    process.start()


if __name__ == "__main__":
    run()

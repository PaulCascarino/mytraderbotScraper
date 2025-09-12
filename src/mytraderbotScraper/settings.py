BOT_NAME = "mytraderbotScraper"

SPIDER_MODULES = ["mytraderbotScraper.spiders"]
NEWSPIDER_MODULE = "mytraderbotScraper.spiders"

# Identification du bot (remplace par ton site si tu veux)
USER_AGENT = "mytraderbotScraper (+https://github.com/PaulCascarino/mytraderbotScraper)"

# Respect robots.txt
ROBOTSTXT_OBEY = True

# Delai entre les requêtes pour éviter de surcharger
DOWNLOAD_DELAY = 1.5

# Pipelines activés
ITEM_PIPELINES = {
    "mytraderbotScraper.pipelines.JsonWriterPipeline": 300,
}

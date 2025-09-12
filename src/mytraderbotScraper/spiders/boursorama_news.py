import scrapy


class BoursoramaNewsSpider(scrapy.Spider):
    name = "boursorama_news"
    allowed_domains = ["boursorama.com"]
    start_urls = ["https://www.boursorama.com/bourse/actualites/"]

    def start_requests(self):
        # Ici on définit combien de pages tu veux parcourir (par ex. 5)
        for page in range(1, 6):
            url = f"https://www.boursorama.com/bourse/actualites/page-{page}"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Chaque ligne d'article
        for article in response.css("li.c-list-news__line"):
            yield {
                "heure": article.css("span.c-list-news__date::text").get(),
                "titre": article.css("p.c-list-news__title a::text").get(),
                "lien": response.urljoin(article.css("p.c-list-news__title a::attr(href)").get()),
                "source": article.css(".c-source__name::text").get(),
            }

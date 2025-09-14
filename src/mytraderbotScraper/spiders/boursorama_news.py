import scrapy


class BoursoramaNewsSpider(scrapy.Spider):
    name = "boursorama_news"
    allowed_domains = ["boursorama.com"]

    def start_requests(self):
        # Ici on définit combien de pages tu veux parcourir (par ex. 9)
        for page in range(1, 3):
            url = f"https://www.boursorama.com/bourse/actualites/page-{page}"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Chaque ligne d'article
        for article in response.css("li.c-list-news__line"):
            item = {
                # On ne prend plus l'heure ici (mais on peut garder pour debug)
                "heure_liste": article.css("span.c-list-news__date::text").get(default="").strip(),
                "titre": article.css("p.c-list-news__title a::text").get(default="").strip(),
                "lien": response.urljoin(article.css("p.c-list-news__title a::attr(href)").get()),
                "source": article.css(".c-source__name::text").get(default="").strip(),
            }
            # On suit le lien vers l'article complet
            if item["lien"]:
                yield scrapy.Request(
                    url=item["lien"],
                    callback=self.parse_article,
                    meta={"item": item},
                )
            else:
                yield item

    def parse_article(self, response):
        item = response.meta["item"]

        # Récupérer la date de publication dans l’article
        item["date"] = response.css(".c-source__time::text").get(default="").strip()

        # Récupérer le texte de l'article
        contenu = response.css(".c-news-detail__content ::text").getall()
        item["article"] = " ".join([c.strip() for c in contenu if c.strip()])

        yield item

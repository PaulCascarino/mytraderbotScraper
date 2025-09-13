# src/mytraderbotScraper/pipelines.py
import polars as pl
from itemadapter import ItemAdapter

DELETE_ARTICLE = "((Traduction automatisée par Reuters à l'aide de l'apprentissage\nautomatique et de l'IA générative, veuillez vous référer à\nl'avertissement suivant: https://bit.ly/rtrsauto))"

class CollectorPipeline:
    collected_items = []

    def process_item(self, item, spider=None):
        # stocke l'item en dict pour compatibilité pandas
        self.collected_items.append(dict(item))
        return item

class CleanArticlePipeline:
    """
    Pipeline qui nettoie chaque item :
    - supprime le champ 'heure_liste'
    - découpe 'date' en 'Date' et 'heure'
    - supprime les disclaimers automatiques Reuters
    """

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # supprimer heure_liste si présent
        if "heure_liste" in adapter:
            adapter.pop("heure_liste")

        # découper date en Date + heure
        if "date" in adapter and isinstance(adapter["date"], str):
            parts = adapter["date"].split(" à ")
            if len(parts) == 2:
                adapter["Date"], adapter["heure"] = parts
            adapter.pop("date", None)

        # nettoyer article
        if "article" in adapter and adapter["article"]:
            cleaned = adapter["article"].replace(DELETE_ARTICLE, "").strip()
            adapter["article"] = cleaned

        return item
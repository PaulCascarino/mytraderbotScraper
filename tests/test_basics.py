# tests/test_basics.py
import os
import polars as pl
from mytraderbotScraper.api import fetch_boursorama_articles

def test_import():
    import mytraderbotScraper
    assert hasattr(mytraderbotScraper, "__version__")

    df = fetch_boursorama_articles(pages=5)  # retourne un pl.DataFrame

    # créer dossier data si besoin
    os.makedirs("./data", exist_ok=True)

    # sauvegarde CSV Polars
    df.write_csv("./data/data.csv", separator=";")

    print(df.head())

if __name__ == "__main__":
    test_import()

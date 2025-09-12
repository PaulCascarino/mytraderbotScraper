# mytraderbotScraper

A Python package based on Scrapy to automatically extract the latest financial news from [Boursorama](https://www.boursorama.com/bourse/actualites/).

## Features

- Scrapes article titles, timestamps, sources, and links  
- Retrieves the full content of each article (`.c-news-detail__content`)  
- Exports JSON encoded in UTF-8 (accents preserved)  
- Provides a dedicated shell command: `scrape-boursorama`  
- Provides a Python API that returns results as a `pandas.DataFrame`  
- Packaged for easy reuse in other projects  

## Installation

Clone the repository and install in development mode:

```bash
git clone https://github.com/PaulCascarino/mytraderbotScraper.git
cd mytraderbotScraper
pip install -e .
```
Or install directly from GitHub:

```bash
pip install git+https://github.com/PaulCascarino/mytraderbotScraper.git
```

## Usage

Activate your virtual environment and run:

```bash
scrape-boursorama
```
This generates a `titres.json` file, for example:

```json
[
  {
    "heure": "20:26",
    "titre": "L'introduction en bourse de StubHub est sursouscrite 20 fois, selon une source",
    "lien": "https://www.boursorama.com/bourse/actualites/l-introduction-en-bourse-de-stubhub...",
    "source": "Reuters",
    "article": "StubHub, qui a retardé son entrée en bourse aux États-Unis..."
  }
]
```

## Usage (Python API)

You can also use the scraper directly inside Python code.
The package provides a function that returns a `pandas.DataFrame`:

```python 
from mytraderbotScraper.api import fetch_boursorama_articles

# Scrape 3 pages of articles
df = fetch_boursorama_articles(pages=3)

print(df.head())
```

Example output:

```bash
   heure                                              titre   source
0  20:26  L'introduction en bourse de StubHub est sursou...  Reuters
1  20:12  Amazon teste des fourgons électriques BrightDrop  Reuters
```

## Development

The project follows a `src/`-based layout:

```css
mytraderbotScraper/
│ pyproject.toml
│ scrapy.cfg
│ README.md
│
├─ src/
│   └─ mytraderbotScraper/
│       ├─ __init__.py
│       ├─ api.py
│       ├─ cli.py
│       ├─ settings.py
│       └─ spiders/
│           └─ boursorama_news.py

```

Run Scrapy directly if needed:

```bash
scrapy crawl boursorama_news -O titres.json
```

## Tests

Run the unit test suite with:

```bash
pytest
```

## License

This project is licensed under the MIT `License`. See the LICENSE file for details.
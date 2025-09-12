# mytraderbotScraper

A Python package based on Scrapy to automatically extract the latest financial news from [Boursorama](https://www.boursorama.com/bourse/actualites/).

## Features

- Scrapes article titles, timestamps, sources, and links  
- Retrieves the full content of each article (`.c-news-detail__content`)  
- Exports JSON encoded in UTF-8 (accents preserved)  
- Provides a dedicated shell command: `scrape-boursorama`  
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
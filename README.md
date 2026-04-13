# Web Scraping Basic

A lightweight web crawler built in Python that recursively crawls a website and extracts page data including headings, links, and images.

## Features

- Recursive crawling up to a configurable depth (default: 2)
- Extracts headings, outgoing links, images, and first paragraph from each page
- Stays within the same domain
- Skips duplicate pages
- Handles timeouts and HTTP errors gracefully
- Stops after 30 pages to avoid overloading servers

## Requirements

- Python 3.12+
- `requests`
- `beautifulsoup4`

## Installation

```bash
git clone https://github.com/zenith0x01/web_scraping_basic.git
cd web_scraping_basic
python3 -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4
```

## Usage

```bash
python3 main.py <url>
```

**Example:**
```bash
python3 main.py https://books.toscrape.com
```

## Example Output

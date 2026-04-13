import sys
import requests
from crawl import crawl_page



def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
        return

    base_url = sys.argv[1]
    page_data = {}

    crawl_page(base_url, base_url, page_data)

    print(f"Crawled {len(page_data)} pages")



if __name__ == "__main__":
    main()

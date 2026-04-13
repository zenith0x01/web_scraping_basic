from urllib.parse import urlsplit, urljoin, urlparse
from bs4 import BeautifulSoup
import requests


def normalize_url(url):
    if not url.startswith("http"):
        url = "https://" + url
    ob = urlsplit(url)
    return (ob.netloc + ob.path).rstrip("/")


def get_heading_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find("h1")
    if h1:
        return h1.get_text()
    h2 = soup.find("h2")
    if h2:
        return h2.get_text()
    return ""


def get_urls_from_html(html, url):
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            fin = urljoin(url, href)
            urls.append(fin.rstrip('/'))
    return urls


def get_images_from_html(html, url):
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for link in soup.find_all("img"):
        imgg = link.get("src")
        if imgg:
            fin = urljoin(url, imgg)
            urls.append(fin.rstrip('/'))
    return urls


def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    p = soup.find("p")
    if p and p.get_text(strip=True):
        return p.get_text(strip=True)
    return ""


def extract_page_data(html, page_url):
    if not page_url.startswith("http"):
        page_url = "https://" + page_url
    res = {}
    res["url"] = page_url.rstrip("/")
    print("URL normalized")
    res["heading"] = get_heading_from_html(html)
    print("Heading extracted")
    res["first_paragraph"] = get_first_paragraph_from_html(html)
    res["outgoing_links"] = get_urls_from_html(html, page_url)
    print("Links extracted")
    res["image_urls"] = get_images_from_html(html, page_url)
    print("Images extracted")
    return res


def get_html(url):
    response = requests.get(
        url,
        headers={"User-Agent": "BootCrawler/1.0"},
        timeout=5
    )
    if response.status_code >= 400:
        raise Exception(f"HTTP error: {response.status_code}")
    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        raise Exception("Invalid content type")
    return response.text


def crawl_page(base_url, start_url, page_data, depth=0, max_depth=2):
    # Queue holds (url, depth) tuples — no recursion, no stack overflow
    queue = [(start_url, depth)]

    while queue:
        current_url, current_depth = queue.pop(0)
        normalized = normalize_url(current_url)

        if normalized in page_data:
            continue
        if current_depth > max_depth:
            continue
        if len(page_data) >= 30:
            break

        print(f"[{current_depth}] Crawling: {current_url}")

        try:
            html = get_html(current_url)
            data = extract_page_data(html, current_url)
            page_data[normalized] = data

            for url in set(data["outgoing_links"]):
                if urlparse(url).netloc != urlparse(base_url).netloc:
                    continue
                if any(x in url for x in ["?", "#"]):
                    continue
                if normalize_url(url) not in page_data:
                    queue.append((url, current_depth + 1))

        except Exception as e:
            print(f"Error crawling {current_url}: {e}")

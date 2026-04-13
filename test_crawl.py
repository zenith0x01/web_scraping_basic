from crawl import (
    normalize_url,
    get_heading_from_html,
    get_urls_from_html,
    get_images_from_html,
    extract_page_data
)
import unittest
class TestCrawl(unittest.TestCase):

    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_get_heading_h1(self):
        html = """
        <html>
          <body>
            <h1>Hello World</h1>
          </body>
        </html>
        """
        self.assertEqual(get_heading_from_html(html), "Hello World")

    def test_get_heading_h2_fallback(self):
        html = """
        <html>
          <body>
            <h2>Fallback Heading</h2>
          </body>
        </html>
        """
        self.assertEqual(get_heading_from_html(html), "Fallback Heading")

    def test_no_heading(self):
        html = "<html><body><p>No heading here</p></body></html>"
        self.assertEqual(get_heading_from_html(html), "")

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)
        
    def test_get_images_from_html(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'

        actual = get_images_from_html(input_body,input_url)
        expected = ['https://crawler-test.com/logo.png']
        self.assertEqual(actual, expected)


    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
        <h1>Test Title</h1>
        <p>This is the first paragraph.</p>
        <a href="/link1">Link 1</a>
        <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
        "url": "https://crawler-test.com",
        "heading": "Test Title",
        "first_paragraph": "This is the first paragraph.",
        "outgoing_links": ["https://crawler-test.com/link1"],
        "image_urls": ["https://crawler-test.com/image1.jpg"]
        }
        self.assertEqual(actual, expected)

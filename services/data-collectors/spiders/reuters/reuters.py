import scrapy
import json
from scrapy.http import TextResponse
from constants import REUTERS_SEARCH_URL
import os

class ReutersSpider(scrapy.Spider):

    name = 'reuters'
    with open("config/selectors_reuters.json", "r") as selector_file:
        selectors = json.load(selector_file)

    def start_requests(self):
        base_url = self.create_reuters_search_url()
        start_urls = [self.create_scrapeops_url(base_url, wait="time")]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: TextResponse, **kwargs):
        # Extract article URLs from the listing page
        urls = response.css(self.selectors['urls']).getall()
        titles = response.css(self.selectors['titles']).getall()
        dates = response.css(self.selectors['dates']).getall()
        topics = response.css(self.selectors['topics']).getall()

        # Yield each article URL with metadata
        for i, url in enumerate(urls):
            yield {
                'url': response.urljoin(url),
                'title': titles[i] if i < len(titles) else None,
                'date': dates[i] if i < len(dates) else None,
                'topic': topics[i] if i < len(topics) else None
            }

    def create_reuters_search_url(self):
        return f"https://www.reuters.com/world"

    def create_scrapeops_url(self, url, js=False, wait=False):
        key = os.getenv("SCRAPEOPS_API_KEY")
        scraping_url = f"https://api.scrapeops.io/v1/scrape?url={url}&api_key={key}"
        if js:
            scraping_url += "&render_js=true"
        if wait:
            scraping_url += f"&wait_for={wait}"
        return scraping_url
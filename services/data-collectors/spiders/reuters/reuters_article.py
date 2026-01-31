import scrapy
import json
from scrapy.http import TextResponse

class ReutersArticleSpider(scrapy.Spider):
    name = 'reuters_article'

    list_of_articles = "output/reuters.csv"
    with open("config/selectors_reuters_article.json", "r") as selector_file:
        selectors = json.load(selector_file)

    def start_requests(self):
        pass

    def parse(self, response: TextResponse, **kwargs):
        pass

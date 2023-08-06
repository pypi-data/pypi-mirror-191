import scrapy

from eintf.common.helper import convert_time, cleanse_html
from eintf.db.db import get_collection


class EtfSpider(scrapy.Spider):
    name = "etf"

    start_urls = [
        "https://etf2l.org",
    ]

    def parse(self, response):
        urls = response.css(".post h1>a[title]::attr(href)")
        for url in urls:
            if get_collection("news").find_one({"url": url.get()}) is not None:
                break
            yield scrapy.Request(url=url.get(), callback=self.get_posts)

    def get_posts(self, response):
        url = response.css("h1 a[href]::attr(href)").get(default='').strip()
        title = response.css("h1 a[href]::text").get(default='').strip()
        date = response.css("h4::text").get(default='').strip().strip()
        author = response.css("a[rel=author]::text").get(default='').strip()
        body = response.css(".etf2l_page").get(default='').strip()
        data = {
            "title": title,
            "date": convert_time(date, "%B %d, %Y"),
            "author": author,
            "url": url,
            "source": self.name,
            "content": cleanse_html(body)
        }
        get_collection("news").insert_one(
            data
        )

    def update(self, process):
        spider = EtfSpider
        process.crawl(spider)


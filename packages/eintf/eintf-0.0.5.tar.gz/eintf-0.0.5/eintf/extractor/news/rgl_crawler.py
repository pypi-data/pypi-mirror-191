import scrapy
from scrapy.crawler import CrawlerProcess

from eintf.common.helper import convert_time, cleanse_html
from eintf.db.db import get_collection


class RglSpider(scrapy.Spider):
    name = "rgl"

    start_urls = [
        "https://rgl.gg/Public/Articles/ArticlesList.aspx",
    ]

    def parse(self, response):
        urls = response.css("#ContentPlaceHolder1_pnlContent a[href*=Default]::attr(href)")[:15]
        for url in urls:
            if get_collection("news").find_one({"url": url.get()}) is not None:
                break
            yield scrapy.Request(url=f"https://rgl.gg/Public/Articles/{url.get()}", callback=self.get_posts)

    def get_posts(self, response):
        title = response.css("span[id*=lblHeader]::text").get(default='').strip()
        body = response.css(".text-center+div[style]+div").get(default='').strip()
        author = response.css("span[id*=lblWriterName]::text").get(default='').strip()
        date = response.css("span[id*=lblDateLive]::text").get(default='').strip()
        data = {
            "title": title,
            "date": convert_time(date, "%m/%d/%Y"),
            "author": author,
            "url": response.url,
            "source": self.name,
            "content": cleanse_html(body)
        }
        get_collection("news").insert_one(
            data
        )

    def update(self, process):
        spider = RglSpider
        process.crawl(spider)


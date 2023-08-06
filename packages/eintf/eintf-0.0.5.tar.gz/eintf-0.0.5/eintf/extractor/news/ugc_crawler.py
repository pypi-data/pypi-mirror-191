import scrapy

from eintf.common.helper import convert_time, cleanse_html
from eintf.db.db import get_collection


class UgcSpider(scrapy.Spider):
    name = "ugc"

    start_urls = [
        "https://www.ugcleague.com/home_tf2h_ALL.cfm",
        "https://www.ugcleague.com/home_tf26_ALL.cfm",
        "https://www.ugcleague.com/home_tf24_ALL.cfm",
        "https://www.ugcleague.com/home_tf22_ALL.cfm",
        "https://www.ugcleague.com/home_atf2h_ALL.cfm",
        "https://www.ugcleague.com/home_atf26_ALL.cfm",
    ]

    def parse(self, response):
        urls = response.css(".col-md-12 p a::attr(href)")
        for url in urls:
            if get_collection("news").find_one({"url": url.get()}) is not None:
                break
            yield scrapy.Request(url=f"https://www.ugcleague.com/{url.get()}", callback=self.get_posts)

    def get_posts(self, response):
        title = response.css(".item-title h4::text").get(default='').strip()
        date_author = response.css(".white-row h5::text").getall()[1].strip()
        date = convert_time(date_author.split("\nby\n")[0].strip(), "%a, %b %d, %Y")
        author = date_author.split(" by ")[1].strip() if " by " in date_author.strip() else ""
        url = f"{response.url}"
        body = response.css(".white-row").get(default='')
        data = {
            "title": title,
            "date": date,
            "author": author,
            "url": url,
            "source": self.name,
            "content": cleanse_html(body).replace('"src', '" src')
        }
        get_collection("news").insert_one(
            data
        )

    def update(self, process):
        spider = UgcSpider
        process.crawl(spider)


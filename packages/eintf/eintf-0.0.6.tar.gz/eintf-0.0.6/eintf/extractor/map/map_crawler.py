import re

import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

from eintf.common.helper import cleanse_html
from eintf.db.db import get_collection


class MapSpider(scrapy.Spider):
    name = "maps"

    def start_requests(self):
        url = "https://tf2maps.net/sitemap-1.xml"
        xml_data = requests.get(url).content
        soup = BeautifulSoup(xml_data, "xml")
        urls = [loc.text for loc in soup.find_all('loc')]
        urls = list(filter(lambda link: "/downloads/" in str(link), urls))
        for url in urls:
            id_ = url.split("/")[-2]
            if get_collection("blacklist").find_one({"data": id_}) is not None:
                continue
            if get_collection("maps").find_one({"id": id_}) is not None:
                continue
            yield scrapy.Request(url=url, callback=self.parse_map)

    def parse_map(self, response):
        if response.css('span[itemprop]::text').get(default='') != "Maps":
            get_collection("blacklist").insert_one(
                {"data": response.url.split("/")[-2], "reason": "not-map"}
            )
            return
        map_info = {
            'id': response.url.split("/")[-2],
            'name': response.css('.p-title-value::text').get(default='').strip(),
            'version': response.css('.p-title-value span::text').get(default='').strip(),
            'author': response.css('.resourceSidebarGroup a[class*=username] span::text').get(default='').strip(),
            'tagline': response.css('.p-tagline-value span::text').get(default='').strip(),
            'firstRelease': int(
                response.xpath("(//div[@class='resourceSidebarGroup']//time)[1]/@data-time").get(default='').strip()),
            'lastUpdate': int(
                response.xpath("(//div[@class='resourceSidebarGroup']//time)[2]/@data-time").get(default='').strip()),
            'category': response.css(".resourceSidebarGroup a[href*='/categories/']::text").get(default='').strip(),
            'downloadUrl': response.xpath(
                "//div[contains(@class,'resourceSidebarGroup')]//div[@class='p-title-pageAction']//a[contains(@href,'/downloads/')]/@href").get(default='').strip(),
            'screens': list(map(lambda it: re.findall(r'\(.*?\)', it)[0].strip("(')"),
                                response.xpath("//div[@class='xfa_ec_img']/@style").getall())),
            'description': cleanse_html(response.css('.bbWrapper').get(default='')),
        }
        get_collection("maps").insert_one(
            map_info
        )

    def update(self):
        process = CrawlerProcess()
        spider = MapSpider
        process.crawl(spider)
        process.start()

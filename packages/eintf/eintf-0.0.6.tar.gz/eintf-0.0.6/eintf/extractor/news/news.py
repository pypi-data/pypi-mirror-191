import traceback

from scrapy.crawler import CrawlerProcess

from eintf.extractor.news.etf_crawler import EtfSpider
from eintf.extractor.news.rgl_crawler import RglSpider
from eintf.extractor.news.ugc_crawler import UgcSpider

valid_sources = ["etf", "rgl", "ugc"]


class News:
    def update(self, sources=None):
        process = CrawlerProcess()
        if sources is None:
            sources = valid_sources
        try:
            if "etf" in sources:
                EtfSpider().update(process)

            if "rgl" in sources:
                RglSpider().update(process)

            if "ugc" in sources:
                UgcSpider().update(process)

            process.start()

            return {"success": True}

        except Exception as e:
            traceback.print_exception(e)
            return {"success": False}

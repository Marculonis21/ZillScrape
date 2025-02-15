from collections.abc import Iterable
import scrapy
import json

class ZillspiderSpider(scrapy.Spider):
    name = "zillspider"
    allowed_domains = ["zillow.com"]
    start_urls = ["https://www.zillow.com/homes/Los-Angeles,-CA_rb/"]

    # def start_requests(self) -> Iterable[scrapy.Request]:
    #     yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        data = response.xpath("//script[@id='__NEXT_DATA__']/text()").get()
        json_data = json.loads(data)

        results = json_data["props"]["pageProps"]["searchPageState"]["cat1"]["searchResults"]["listResults"]
        for res in results:
            if res.get("hasOpenHouse", False):
                yield res

        pagination = json_data["props"]["pageProps"]["searchPageState"]["cat1"]["searchList"]["pagination"]
        next = pagination.get("nextUrl", None)
        if next:
            print("NEXT", next)
            yield response.follow(next, callback=self.parse)



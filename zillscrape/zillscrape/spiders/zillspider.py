from collections.abc import Iterable
from typing import Counter
import scrapy
import json
from scrapy_playwright.page import PageMethod
from zillscrape.items import ZillscrapeItem

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
                item = ZillscrapeItem()

                item["zpid"       ] = res.get("zpid", None),
                item["imgSrc"     ] = res.get("imgSrc", None),
                item["detailUrl"  ] = res.get("detailUrl", None),
                item["price"      ] = res.get("price", None),
                item["address"    ] = res.get("address", None),
                item["latLong"    ] = res.get("latLong", None),
                item["brokerName" ] = res.get("brokerName", None),

                yield scrapy.Request(res.get("detailUrl"), callback=self.parse_details, cb_kwargs={'item':item})

        pagination = json_data["props"]["pageProps"]["searchPageState"]["cat1"]["searchList"]["pagination"]
        next = pagination.get("nextUrl", None)
        if next:
            print("NEXT", next)
            yield response.follow(next, callback=self.parse)


    def parse_details(self, response, item):
        description = response.xpath("//div[@data-testid='description']/article/div/div/text()").get()

        if description == None:
            yield scrapy.Request(response.url, callback=self.parse_js_details, cb_kwargs={'item': item}, meta={"playwright": True,
                                                                                                            "playwright_page_methods": [
                                                                                                                PageMethod("wait_for_selector","button.Anchor-c11n-8-100-1__sc-hn4bge-0.cinxUv"),
                                                                                                                PageMethod("click","button.Anchor-c11n-8-100-1__sc-hn4bge-0.cinxUv")
                                                                                                            ]}, dont_filter=True)
        else :
            item["description"] = description

            yield item

    def parse_js_details(self, response, item):
        description = response.xpath("//p[@data-testid='property-description']/text()").get()

        item["description"] = description
        yield item

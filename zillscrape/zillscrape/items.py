# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ZillscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    zpid = scrapy.Field()
    imgSrc = scrapy.Field()
    detailUrl = scrapy.Field()
    price = scrapy.Field()
    address = scrapy.Field()
    latLong = scrapy.Field()
    brokerName = scrapy.Field()
    description = scrapy.Field()

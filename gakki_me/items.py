# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class SongPages(scrapy.Item):
    song_urls = scrapy.Field()

class CodesLyrics(scrapy.Item):
    titles = scrapy.Field()
    lyrics = scrapy.Field()
    codes  = scrapy.Field()

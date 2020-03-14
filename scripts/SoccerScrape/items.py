# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Player(scrapy.Item):
    rosterYear = scrapy.Field()
    firstName = scrapy.Field()
    lastName = scrapy.Field()
    classYear = scrapy.Field()
    position = scrapy.Field()
    homeTown = scrapy.Field()
    state_or_country = scrapy.Field()
    highSchool       = scrapy.Field()
    college          = scrapy.Field()
    collegeLeague    = scrapy.Field()
    height           = scrapy.Field()
    previousSchool   = scrapy.Field()
    profileLink      = scrapy.Field()
    number           = scrapy.Field()
    weight           = scrapy.Field()

class Starter(scrapy.Item):
    rosterYear      = scrapy.Field()
    firstName       = scrapy.Field()
    lastName        = scrapy.Field()
    potentialStarts = scrapy.Field()
    starts          = scrapy.Field()
    plays           = scrapy.Field()
    isStarter       = scrapy.Field()
    school          = scrapy.Field()
    number          = scrapy.Field()


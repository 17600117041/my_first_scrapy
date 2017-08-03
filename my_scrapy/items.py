# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    movie_name = scrapy.Field() #电影名字
    score_num = scrapy.Field() #评分
    ranking = scrapy.Field()
    score = scrapy.Field()
    pass

class ZhihuItem(scrapy.Item):
    url = scrapy.Field()  # 保存抓取问题的url
    title = scrapy.Field()  # 抓取问题的标题
    description = scrapy.Field()  # 抓取问题的描述
    answer = scrapy.Field()  # 抓取问题的答案
    name = scrapy.Field()  # 个人用户的名称
    pass






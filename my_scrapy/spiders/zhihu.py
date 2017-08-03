# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, FormRequest
from scrapy.selector import Selector
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from my_scrapy.items import ZhihuItem
import time
from PIL import Image
import os
import pytesser3
import pytesseract

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/question']

    rules = (
        Rule(LinkExtractor(allow=('/question/\d+#.*?', )), callback= 'parse_page_new', follow= True),
    )
    # def parse(self, response):
    #     pass

    headers = {
        'Host' :"www.zhihu.com",
        'User-Agent' : "Mozilla/5.0 (Macintosh; Intel… Gecko/20100101 Firefox/54.0",
        'Accept' : "*/*",
        'Accept-Language' : "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        'Accept-Encoding' : "gzip, deflate, br",
        'X-Requested-With' : "XMLHttpRequest",
        'Referer' : "https://www.zhihu.com/",
        'Connection' : "keep-alive",
    }

    def start_requests(self):
        t = str(int(time.time() * 1000))
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + '&type=login&lang=en'
        return [scrapy.Request(url=captcha_url, headers=self.headers, callback=self.parser_captcha)]
        # return [Request("https://www.zhihu.com/#signin",meta= {'cookiejar' : 1},callback= self.postLogin)]

    def parser_captcha(self,response):
        with open('captcha.jpg','wb') as f:
            f.write(response.body)
            f.close()
        # try:
        im = Image.open('captcha.jpg')
        str = pytesseract.image_to_string(im)
        print(str)
        #     im.show()
        #     im.close()
        # except:
        print("请到 %s 目录 查看captcha.jpg 手动输入" %  os.path.abspath('captcha.jpg'))
        captcha = input("please input the captcha\n>")
        return [scrapy.Request(url='https://www.zhihu.com/#signin',headers=self.headers,meta={'captcha' : captcha},callback=self.postLogin)]

    def handle_captcha(self,image):
        pass

    def postLogin(self,response):
        print(" preparing  login")
        #抓取表单验证时 需要的  _xsrf字段的内容 用于提交表单
        xsrf = response.xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print(xsrf)
        # FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        # 登陆成功后, 会调用after_login回调函数
        return [FormRequest.from_response(response, url = "https://www.zhihu.com/login/phone_num",
            # meta = { 'cookiejar' : response.meta['cookiejar']},
            headers = self.headers,
            formdata= {
                '_xsrf' : xsrf,
                'password': "love@5807891",
                'captcha_type': "en",
                'phone_num': "18624394840",
                'captcha': response.meta['captcha'],
            },callback = self.after_login,
            # dont_filter=True
        )]

    def after_login(self,response):
        print(response.body)
        for url in self.start_urls:
            print(url)
            yield self.make_requests_from_url(url)

    def parse(self,response):
        items = ZhihuItem()
        items['url'] = response.url
        items['name'] = response.xpath('//span[@class="name"]/text()').extract()
        print(items['name'])
        items['title'] = response.xpath('//h2[@class="zm-item-title zm-editable-content"]/text()').extract()
        items['description'] = response.xpath('//div[@class="zm-editable-content"]/text()').extract()
        items['answer'] = response.xpath('//div[@class=" zm-editable-content clearfix"]/text()').extract()
        return items

# -*- coding:utf-8 -*-
import json
from lxml import etree
import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http import HtmlResponse, TextResponse
from moduowang.items import ModuowangItem
from moduowang.mysqlpipelines.pipelines import MySQLStorePipeline


class ModuoSpider(scrapy.Spider):

    name = 'moduowang'
    allowed_domains = ["moduovr.com"]
    start_urls = [
        "http://www.moduovr.com/category/40.html"
    ]

    # 全局参数，定义起始页码和总页码
    total_page = 129
    page = 2

    def parse(self, response):
        items = []
        for info in response.xpath('//div[@class="caption"]'):
            item = ModuowangItem()
            item['name'] = info.xpath('a/h1/text()').extract()
            item['url'] = info.xpath('a/@href').extract()
            item['tag'] = info.xpath('div[@class="meta"]/a/text()').extract()
            # normalize-space去掉空格和换行符
            item['time'] = info.xpath('normalize-space(div[@class="row-table hidden-xs"]/div[@class="col-table-cell col-12"]/div[@class="data"]/span/text())').extract()
            # item['id'] = info.xpath('a/@href').extract().sqlit('/')[-1].sqlit('.')[0]
            items.append(item)
            yield item
            # # 如果存在重复的内容就停止爬虫
            # if not MySQLStorePipeline.tag:
            #     pass
            next_url = "http://www.moduovr.com/front/welcome/article_list?page=2&limit=20"
        # 这里的请求就是点击下一页，发送获取下一页的请求
        yield scrapy.Request(next_url, self.parse_json)

    # 获取返回的下一页json格式的数据（需要分析请求）
    def get_json_response(self, response):
        # total_page = 10
        # page = 2
        js = json.loads(response.body)
        # 由于moduo网部分页面采用的ajax请求，翻页是点击“下一页”进行翻页，而翻页的请求是一个ajax请求，且返回的结果在浏览器查看显示乱码，不是标准的json文件
        # 后通过fiddler进行查看，发现，发送的下一页ajax请求是有返回一个json格式的字典数据，包含一个模板（template）以及全部页面total_page
        # 通过获取到返回的json，然后通过key值'template'即可获取到想要的下一页html数据（这与其它页面有点区别）
        # 先前的解决方案是借助selenium + phantomJS模拟浏览器行为，但是在获取页面信息的时候容易出现内存爆掉的情况
        html = js['template']
        # 这里将返回的数据转换一下编码格式方便接下来的操作（不然会提示：Unicode 没有xpath）
        html = html.encode('utf-8')
        # html = HtmlXPathSelector(html)
        # html.select('//div[]@class="col-table-cell align-top hidden-xs"]')
        if self.page < self.total_page & MySQLStorePipeline.tag == True:
            # html_response = HtmlResponse("http://www.moduovr.com/front/welcome/article_list?page=2&limit=20", body=html)
            # 为了将获得的下一页数据处理成可xpath的html格式，使用如下方法
            html_response = HtmlResponse("http://www.moduovr.com/front/welcome/article_list?limit=20&page=" + str(self.page), body=html)
            hxs = HtmlXPathSelector(html_response)
            desc = hxs.xpath('//div[@class="caption"]')
        self.page = self.page + 1
        return desc

    # 对获取到的json格式的报文进行解析，获取到的模板和页面结构是一样的所以解析的方法一样
    def parse_json(self, response):
        items = []
        json_html = self.get_json_response(response)
        # js = json.loads(response.body)
        # html = js['template']
        # html = html.encode('utf-8')
        # # html = HtmlXPathSelector(html)
        # # html.select('//div[]@class="col-table-cell align-top hidden-xs"]')
        # html_response = HtmlResponse("http://www.moduovr.com/front/welcome/article_list?page=2&limit=20", body=html)
        # hxs = HtmlXPathSelector(html_response)
        # desc = hxs.xpath('//div[@class="caption"]')
        for info in json_html:
            item = ModuowangItem()
            item['name'] = info.xpath('a/h1/text()').extract()
            item['url'] = info.xpath('a/@href').extract()
            item['tag'] = info.xpath('div[@class="meta"]/a/text()').extract()
            # normalize-space去掉空格和换行符
            item['time'] = info.xpath('normalize-space(div[@class="row-table hidden-xs"]/div[@class="col-table-cell col-12"]/div[@class="data"]/span/text())').extract()
            # item['id'] = info.xpath('a/@href').extract().sqlit('/')[-1].sqlit('.')[0]
            items.append(item)
            yield item

        next_url = "http://www.moduovr.com/front/welcome/article_list?limit=20&page=" + str(self.page)
        # 回调parse_json方法，递归处理接下来的页面
        yield scrapy.Request(next_url, self.parse_json)






















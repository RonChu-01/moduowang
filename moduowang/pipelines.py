# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import os

class JsonWithEncodingCnblogsPipeline(object):

    def __init__(self):
        if not os.path.isfile('moduo.json'):
            # 注意这里json格式文件的打开方式，"w"是以写的形式打开，会覆盖，"a"是以追加的形式打开
            self.file = codecs.open('moduo.json', 'w', encoding='utf-8')
            print "新建json文件"
        else:
            self.file = codecs.open('moduo.json', 'a', encoding='utf-8')
            print "文件已存在，追加"

    def process_item(self, item, spider):
        # 爬取的内容存在空的情况，判断过滤一下
        if not item['name'] == []:
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()
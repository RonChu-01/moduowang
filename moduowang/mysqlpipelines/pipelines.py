# -*- coding: utf-8 -*-

from .sql import Sql
from moduowang.items import ModuowangItem

class MySQLStorePipeline(object):

    tag = True

    def process_item(self, item, spider):

        if isinstance(item, ModuowangItem):
            url = item['url'][0]
            ret = Sql.select_url_id(url)
            if ret[0] == 1:
                print ('已经存在了')
                self.tag = False
                pass
            else:
                Sql.insert_into_table(item)
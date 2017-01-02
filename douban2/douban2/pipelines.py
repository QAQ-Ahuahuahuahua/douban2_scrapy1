# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import pymysql

def dbConnent():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        passwd='zjh418',
        db='douban',
        charset='utf8',
        use_unicode=False
    )
    return conn

class MySQLPipeline(object):

    def process_item(self,item,spider):
        db = dbConnent()
        cursor = db.cursor()
        sql = 'insert into doing_comment(userName,credit,grade,time,comment) values("%s","%s","%d","%s","%s")'
        values = (item['userName'], item['credit'], item['grade'], item['time'], item['comment'])
        #values =('haha','hahah',1,'hahah','hahah')
        try:
            # 执行sql语句
            cursor.execute(sql % values)
            db.commit()
        except:
            # 发生错误时回滚
            print("出错")
            db.rollback()
        finally:
            # 关闭数据库连接
            # cursor.close()  # 关闭游标
            db.close()
        return item


class Douban2Pipeline(object):

    def __init__(self):
        self.file = codecs.open('comment.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line + ',')
        return item

    def spider_closed(self, spider):
        self.file.close()

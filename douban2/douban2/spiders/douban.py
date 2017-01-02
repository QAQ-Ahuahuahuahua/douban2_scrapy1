#coding = utf-8
import scrapy
from douban2.items import Douban2Item

#豆瓣评分等级
gradeDic = {
    '力荐':5,
    '推荐':4,
    '还行':3,
    '较差':2,
    '很差':1
}

class DouBan(scrapy.Spider):
    name = 'douban'

    #起始url，一个是正在看部分的评论，一个是看过部分的评论
    start_urls = [
        'https://movie.douban.com/subject/26345137/doings?start=0',
        'https://movie.douban.com/subject/26345137/collections?start=0'
    ]

    def parse(self, response):

        contents = response.xpath('//div[@class="sub_ins"]/table') #获得用户评论区域
        if contents:
            for content in contents:
                #获取用户名
                name = content.xpath('tr/td[2]/div/a/text()').extract()[0].replace(' ', '').replace('\n', '')
                #获取评论时间并格式化
                time = content.xpath('tr/td[2]/p/text()').extract()[0].replace(' ', '').replace('\n', '').replace(
                    '\xa0', '')
                #判断用户是否打分，如果没有直接跳过
                if content.xpath('tr/td[2]/p/span[contains(@class,"allstar")]'):
                    item = Douban2Item()
                    #获取用户评级
                    credit = content.xpath('tr/td[2]/p/span[contains(@class,"allstar")]/@title').extract()[0]
                    item['userName'] = name
                    item['credit'] = credit
                    item['grade'] = gradeDic[credit]
                    item['time'] = time
                    #获取用户评论
                    comment = content.xpath('tr/td[2]/p[2]/text()')
                    if comment:
                        item['comment'] = comment.extract()[0]
                    else:
                        item['comment'] = ''
                    yield item
            #获取下一页url
            nextPage = response.xpath('//span[@class="next"]/a/@href')
            if nextPage:
                url = nextPage.extract()[0]
                print(url)
                yield scrapy.Request(url,self.parse)
        else:
            print("已经是最后一页")

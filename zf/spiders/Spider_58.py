import re
import scrapy
from scrapy.http import Request

from zf.items import ZfItem


class Spider_58(scrapy.Spider):

    name = 'spider_58'
    allowed_domains = ['sz.58.com', 'jxjump.58.com']
    start_urls = [
        "https://sz.58.com/chuzu/"
    ]

    def start_requests(self):
        """
        这是一个重载函数，它的作用是发出第一个Request请求
        :return:
        """
        # 请求self.start_urls[0],返回的response会被送到回调函数parse中
        yield Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):
        max_page_text = response.xpath('//li[@id="pager_wrap"]/div[@class="pager"]/a[last()-1]/span/text()').extract()
        max_num = int(max_page_text[0])
        print('max page>>>>>>>>>>>', max_num)
        # for i in range(max_num):
        #     print(i)
        #     url = self.start_urls[0] + 'pn' + str(i + 1) + '/'
        #     # 该方法及其他的Request回调函数必须返回一个包含 Request 及(或) Item 的可迭代的对象
        #     yield Request(url, callback=self.extract_list, priority=max_num - i)
        url = self.start_urls[0] + 'pn1/'
        yield Request(url, callback=self.parse_list)

    def parse_list(self, response):
        links = response.xpath('//ul[@class="house-list"]/li[@class="house-cell"]/div[@class="img-list"]/a/@href')
        # for link in links:
        #     yield Request(link.extract(), callback=self.extract_detail)
        link = links[0].extract()
        matchObj = re.match(r'.*&entinfo=(.*?)&.*', link)
        id = matchObj.group(1)
        yield Request(link, callback=self.parse_detail, meta={'id': id})

    def parse_detail(self, response):
        id = response.meta['id']
        item = ZfItem()
        item['id'] = id
        item['name'] = response.xpath('//div[@class="house-title"]/h1/text()').extract()[0]
        item['price'] = response.xpath('//div[@class="house-pay-way f16"]/span[1]/b/text()').extract()[0]
        item['housing_estate'] = response.xpath('//div[@class="house-basic-desc"]//li[last()-2]/span[2]/a/text()').extract()[0]

        img_paths = response.xpath('//div[@class="basic-pic-list pr"]//li/img/@data-src')
        imgs = []
        for img_path in img_paths:
            # //pic5.58cdn.com.cn/anjuke_58/425f80a6eb3f981227ede035cc9758b4
            # //pic5.58cdn.com.cn/anjuke_58/425f80a6eb3f981227ede035cc9758b4?w=640&h=480&crop=1
            img_src = img_path.extract()
            img_src = re.match(r'//(.*?)\?.*', img_src).group(1)
            imgs.append('https://' + img_src)
        item['image_urls'] = imgs

        area_paths = response.xpath('//div[@class="house-basic-desc"]//li[last()-1]/span[2]/a/text()').extract()
        area = ''
        for a in area_paths:
            area += str(a).strip() + ' '
        item['area'] = area

        addr = response.xpath('//div[@class="house-basic-desc"]//li[last()]/span[@class="dz"]/text()').extract()[0]
        addr = str(addr).strip()
        item['address'] = addr

        point_paths = response.xpath('//ul[@class="introduce-item"]/li[1]/span[2]/em/text()').extract()
        point = ''
        for p in point_paths:
            point += str(p).strip() + ' '
        item['housing_point'] = point

        desc_paths = response.xpath('//ul[@class="introduce-item"]/li[2]//li/span/text()').extract()
        desc = ''
        for p in desc_paths:
            desc += str(p).strip() + '\n'
        item['desc'] = desc

        yield item

import re
import scrapy
from scrapy.http import Request

from zf.items import ZfItem


class Spider_58(scrapy.Spider):

    name = 'spider_58_house'
    allowed_domains = ['58.com', 'jxjump.58.com']
    start_urls = [
        "https://sz.58.com/pinpaigongyu/"
    ]

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):
        links = response.xpath('//div[@class="main"]//ul[@class="list"]/li/a/@href')
        for link in links:
            url = link.extract()
            matchObj = re.match(r'.*tid=(.*?)', url)
            id = matchObj.group(1)
            yield Request(url, callback=self.parse_detail, meta={'id': id})
        # link = links[0].extract()
        # matchObj = re.match(r'.*&entinfo=(.*?)&.*', link)
        # id = matchObj.group(1)
        # yield Request(link, callback=self.parse_detail, meta={'id': id})

    def parse_detail(self, response):
        id = response.meta['id']
        item = ZfItem()
        item['id'] = id
        # item['name'] = response.xpath('//div[@class="house-title"]/h1/text()').extract()[0]
        # item['price'] = response.xpath('//div[@class="house-pay-way f16"]/span[1]/b/text()').extract()[0]
        # item['housing_estate'] = response.xpath('//div[@class="house-basic-desc"]//li[last()-2]/span[2]/a/text()').extract()[0]

        img_paths = response.xpath('//div[@class="basic-pic-list pr"]//li/img/@src')
        imgs = []
        for img_path in img_paths:
            img_src = img_path.extract()
            img_src = re.match(r'//(.*?)\?.*', img_src).group(1)
            imgs.append(img_src)
        item['image_urls'] = imgs

        # area_paths = response.xpath('//div[@class="house-basic-desc"]//li[last()-1]/span[2]/a/text()').extract()
        # area = ''
        # for a in area_paths:
        #     area += str(a).strip() + ' '
        # item['area'] = area

        # addr = response.xpath('//div[@class="house-basic-desc"]//li[last()]/span[@class="dz"]/text()').extract()[0]
        # addr = str(addr).strip()
        # item['address'] = addr

        # point_paths = response.xpath('//ul[@class="introduce-item"]/li[1]/span[2]/em/text()').extract()
        # point = ''
        # for p in point_paths:
        #     point += str(p).strip() + ' '
        # item['housing_point'] = point

        # desc_paths = response.xpath('//ul[@class="introduce-item"]/li[2]//li/span/text()').extract()
        # desc = ''
        # for p in desc_paths:
        #     desc += str(p).strip() + '\n'
        # item['desc'] = desc

        yield item

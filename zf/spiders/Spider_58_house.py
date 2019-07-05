import re
import scrapy
from scrapy.exceptions import DropItem

from scrapy.http import Request

import db
from zf.items import ZfItem


class Spider_58_house(scrapy.Spider):

    name = 'spider_58_house'
    allowed_domains = ['58.com', 'jxjump.58.com']
    start_urls = [
        "https://sz.58.com/pinpaigongyu/"
    ]

    def start_requests(self):
        page_count = 70
        for i in range(1, page_count):
            page_url = "https://sz.58.com/pinpaigongyu/pn/%s/" % i
            yield Request(page_url, callback=self.parse_list)

    def parse_list(self, response):
        links = response.xpath('//div[@class="main"]//ul[@class="list"]/li/a/@href')
        for link in links:
            url = link.extract()
            yield Request(url, callback=self.parse_detail)
        # url = links[0].extract()
        # yield Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        # https://sz.58.com/pinpaigongyu/38616137526808x.shtml?adtype=1&tid=035a5f79-bd52-4a69-871d-007592f52736
        url = response.request.url
        matchObj = re.match(r'.*/pinpaigongyu/(.*?)x.shtml', url)
        id = matchObj.group(1)

        num = db.query_count('select count(*) from house where id=?', id)
        if num > 0:
            raise DropItem("Duplicate item found: %s" % id)

        item = ZfItem()
        item['id'] = id
        item['source'] = '58同城-品牌公寓'
        item['name'] = response.xpath('//title/text()').extract()[0]
        # item['price'] = str(response.xpath('//div[@class="house-title-wrap"]//span[@class="price strongbox"]/text()').extract()[0]).strip()
        # item['housing_estate'] = str.join(' ', response.xpath('//div[@class="housedetail center cf"]//a/text()').extract())

        img_paths = response.xpath('//div[@class="house-title-wrap"]//img/@src')
        if len(img_paths) == 0:
            img_paths = response.xpath('//div[@class="basic-pic-list pr"]//img/@src')
        imgs = []
        for img_path in img_paths:
            img_src = img_path.extract()
            img_src = re.match(r'//(.*?)\?.*', img_src).group(1)
            imgs.append('https://' + img_src)
        item['image_urls'] = imgs

        # area_paths = response.xpath('//div[@class="house-basic-desc"]//li[last()-1]/span[2]/a/text()').extract()
        # area = ''
        # for a in area_paths:
        #     area += str(a).strip() + ' '
        # item['area'] = area

        # addr = response.xpath('//ul[@class="house-info-list"]//li[4]//span/text()').extract()[0]
        # addr = str(addr).strip()
        # item['address'] = addr
        #
        # item['housing_point'] = str.join(' ', response.xpath('//ul[@class="tags-list"]//li/text()').extract())
        #
        # descs = response.xpath('//div[@class="desc-wrap"]//p/text()').extract()
        # descs = map(lambda s: s.strip(), descs)
        # item['desc'] = str.join('\n', descs)

        yield item

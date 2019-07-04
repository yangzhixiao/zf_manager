# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import os

import xlwt as xlwt
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes


class ZfPipeline(object):
    def process_item(self, item, spider):
        return item


class Pipeline_58(object):
    def __init__(self):
        self.filename = './58_houses.xls'
        self.outputbook = xlwt.Workbook()
        self.table = self.outputbook.add_sheet('sheet1', cell_overwrite_ok=True)
        self.nrow = 0

    def process_item(self, item, spider):
        self.table.write(self.nrow, 0, item['name'])
        self.table.write(self.nrow, 1, item['price'])

        self.nrow += 1

    def close_spider(self, spider):
        self.outputbook.save(self.filename)


class MyImagePipeline(ImagesPipeline):

    id = ''

    def get_media_requests(self, item, info):
        self.id = item['id']
        return [Request(x) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)

        image_guid = hashlib.sha1(to_bytes(url)).hexdigest()
        return '%s/%s.jpg' % (self.id, image_guid)

    def thumb_path(self, request, thumb_id, response=None, info=None):
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.thumb_key(url) method is deprecated, please use '
                          'thumb_path(request, thumb_id, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from thumb_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        image_guid = hashlib.sha1(to_bytes(url)).hexdigest()
        return '%s/thumb/%s.jpg' % (self.id, image_guid)

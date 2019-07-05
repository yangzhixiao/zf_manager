# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib

from scrapy.utils.misc import md5sum

import db

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes


class ZfPipeline(object):
    def process_item(self, item, spider):
        return item


class DbPipeline(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):
        id = item['id']
        images = str.join(',', map(lambda i: i['path'], filter(lambda i: i['checksum'] is not None, item['images'])))
        source = item['source']
        addtime = item['addtime']
        title = str(item['name']).strip()
        db.execute(
            'insert into house (id, title, imgs, source, addtime) values (?, ?, ?, ?, ?)',
            id, title, images, source, addtime
        )
        return item

    def close_spider(self, spider):
        db.close()


class MyImagePipeline(ImagesPipeline):

    id = ''
    date = ''

    def get_media_requests(self, item, info):
        self.id = item['id']
        self.date = item['addtime']
        return [Request(x) for x in item.get(self.images_urls_field, [])]

    def image_downloaded(self, response, request, info):
        checksum = None
        for path, image, buf in self.get_images(response, request, info):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            width, height = image.size

            if (width > 600 or width == 200) or (height > 600 or height == 200):
                self.store.persist_file(
                    path, buf, info,
                    meta={'width': width, 'height': height},
                    headers={'Content-Type': 'image/jpeg'})
            else:
                return None
        return checksum

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
        return '%s/%s/%s.jpg' % (self.date, self.id, image_guid)

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
        return '%s/%s/thumb/%s.jpg' % (self.date, self.id, image_guid)

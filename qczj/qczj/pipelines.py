# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from qczj.settings import IMAGES_STORE
import os

class DownimgPipeline(object):
    def process_item(self, item, spider):
        return item


class BMWImagePipline(ImagesPipeline):
    def get_media_requests(self, item, info):
        request_objs = super(BMWImagePipline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        path = super(BMWImagePipline, self).file_path(request, response, info)
        name = request.item.get('name')
        name_path = os.path.join(IMAGES_STORE, name)
        if not os.path.exists(name_path):
            os.mkdir(name_path)
        type = request.item.get('type')
        type_path = os.path.join(name_path, type)
        if not os.path.exists(type_path):
            os.mkdir(type_path)
        image_name = path.replace("full/","")
        image_path = os.path.join(type_path, image_name)
        return image_path

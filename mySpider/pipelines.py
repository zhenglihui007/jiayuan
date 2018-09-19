# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.utils.project import get_project_settings
from scrapy.pipelines.images import ImagesPipeline
# import shutil
import scrapy
# import os
import re
# from scrapy import Request
import codecs
import json

class MyspiderPipeline(ImagesPipeline):
    img_store = get_project_settings().get("IMAGES_STORE")
    # def __init__(self):
    #     self.jsname = codecs.open('sunwz.json', 'w', encoding='utf-8')

    def get_media_requests(self, item, info):
        img_url = item['img']
        print("提取------" + str(item['name']) + "------的图片链接并提交下载")
        # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
        for url in img_url:
            # meta里面的数据是从spider获取，然后通过meta传递给下面方法：file_path
            yield scrapy.Request(url, meta={'name':item['name']})

    # 重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字
    def file_path(self, request, response=None, info=None):
        # 提取url前面名称作为图片名。
        image_guid = request.url.split('/')[-1]
        # 接收上面meta传递过来的图片名称
        name = request.meta['name']
        # 过滤windows字符串，不经过这么一个步骤，你会发现有乱码或无法下载
        name = re.sub(r'[？\\*|“<>:/]', '', name)
        # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
        filename = u'{0}/{1}'.format(name, image_guid)

        return filename
    # 重写item_completed方法
    # 将下载的文件保存到不同的目录中
    def item_completed(self, results, item, info):
        image_path = [x["path"] for ok, x in results if ok]
        if not image_path:
            raise DropItem("Item contains no files")
        jsname = codecs.open(self.img_store + '/' + item['name'] + '/' + item['name'] + '.json', 'w', encoding='utf-8')
        content = json.dumps(dict(item), ensure_ascii=False) + "\n"
        jsname.write(content)
        print("保存图片和数据到-------" + str(item['name']))
        # # 定义分类保存的路径
        # img_path = "%s/%s" % (self.img_store, item['name'])  # item['name']
        # # 目录不存在则创建目录
        # if os.path.exists(img_path) == False:
        #     os.mkdir(img_path)
        #
        # print("--" * 30)
        # print(self.img_store + image_path[0])
        # print(img_path + "\\" + item["img_name"] + '.jpg')
        # # 将文件从默认下路路径移动到指定路径下
        # shutil.move(self.img_store + "\\" + image_path[0], img_path + "\\" + image_path[0][image_path[0].find("full\\")+6:])
        #
        # item["img_path"] = img_path + "\\" + image_path[0][image_path[0].find("full\\")+6:]
        return item





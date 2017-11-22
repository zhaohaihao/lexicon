#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: URLGrapTool.py

"""
Created on 2017/11/21 0021

@author: bigsea
"""

from pyquery import PyQuery as pq
from requests.exceptions import RequestException
import math
import time
import re
import DBTool

# 基础链接
SOGOU_MAIN_URL_BASE = 'http://pinyin.sogou.com'
# 入口链接
ENTRANCE_URL = 'https://pinyin.sogou.com/dict/cate/index/167'
# 一级分类种类
ONE_LEVEL_TYPE = [
    '城市信息', '自然科学', '社会科学', '工程应用',
    '农林渔畜', '医学医药', '电子游戏', '艺术设计',
    '生活百科', '运动休闲', '人文科学', '娱乐休闲'
]
# 每页个数
NUM_COUNT = 10

"""
搜狗词库URL抓取器
"""
class URLGrapMachine:
    def get_one_level_url(self):
        """
        获取一级分类数据所有url
        :return: 
        """
        try:
            print(">>> 获取一级分类数据所有的URL开始! >>>")
            type_url = []
            doc = pq(url=ENTRANCE_URL)
            for item in doc("#dict_nav_list li a").items():
                type_url.append(item.attr('href'))
            for i in range(len(ONE_LEVEL_TYPE)):
                saveEntity = {
                    'typeName': ONE_LEVEL_TYPE[i],
                    'typeUrl': SOGOU_MAIN_URL_BASE + type_url[i],
                    "createtime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                }
                print(saveEntity)
                DBTool.DBTool().save_oneLevelData2mongoDB(saveEntity)
            print(">>> 获取一级分类数据所有的URL结束! >>>")
        except RequestException as e:
            print(">>> 获取一级分类数据所有的URL过程中发生异常, 请检查后重新获取! >>>")
            print(">>> 异常信息 >>>", e.strerror)

    def get_two_level_url(self):
        """
        获取二级分类数据所有url
        :return: 
        """
        try:
            print(">>> 获取二级分类数据所有的URL开始! >>>")
            oneLevelList = DBTool.DBTool().get_oneLevelData()
            # 如果一级分类数据为空则请求
            if oneLevelList.count() == 0:
                URLGrapMachine().get_one_level_url()
            for oneLeveInfo in oneLevelList:
                oneLevelTypeUrl = oneLeveInfo['typeUrl']
                oneLevelTypeName = oneLeveInfo['typeName']
                oneDoc = pq(url=oneLevelTypeUrl)
                print(">>> 当前二级分类:", oneLevelTypeName, "信息获取开始!>>> ")
                if oneLevelTypeName == "城市信息":
                    # 城市信息单独处理
                    for oneItem in oneDoc(".city_list .citylist").items():
                        oneItemUrl = SOGOU_MAIN_URL_BASE + oneItem.attr('href')
                        oneItemName = oneItem.text()
                        twoDoc = pq(url=oneItemUrl)
                        tdList = []
                        # 三级分类列表
                        subList = []
                        for thirdItem in twoDoc(".cate_words_list tr .cate_num_font").items():
                            subList.append(thirdItem)
                        if len(subList):
                            # 如果包含三级分类
                            for thirdItem in twoDoc(".cate_words_list tr .cate_num_font").parents("a").items():
                                thirdTypeUrl = SOGOU_MAIN_URL_BASE + thirdItem.attr('href')
                                thirdTypeName = thirdItem.text().split(' (')[0:1][0]
                                count = thirdItem.text().split(' (')[1:][0][:-1]
                                pageNum = math.ceil(int(count) / NUM_COUNT)
                                saveEntity = {
                                    "url": thirdTypeUrl,
                                    "page": pageNum,
                                    "type1": oneLevelTypeName,
                                    "type2": oneItemName,
                                    "type3": thirdTypeName,
                                    "count": int(count),
                                    "createtime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                                }
                                print(">>> 信息正在入库 >>> ", saveEntity)
                                DBTool.DBTool().save_twoLevelData2mongoDB(saveEntity)
                        else:
                            # 如果不包含三级分类
                            str = twoDoc(".cate_title")[0].text
                            page = re.findall("\d+", str)[0]
                            pageNum = math.ceil(int(page) / NUM_COUNT)
                            saveEntity = {
                                "url": oneItemUrl,
                                "page": pageNum,
                                "type1": oneLevelTypeName,
                                "type2": oneItemName,
                                "type3": "",
                                "count": int(page),
                                "createtime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                            }
                            print(">>> 信息正在入库 >>>", saveEntity)
                            DBTool.DBTool().save_twoLevelData2mongoDB(saveEntity)
                else:
                    # 其他信息处理
                    # 无子节点
                    for oneItem in oneDoc(".cate_no_child a").items():
                        url = SOGOU_MAIN_URL_BASE + oneItem.attr('href')
                        name = oneItem.text().split(' (')[0:1][0]
                        count = oneItem.text().split(' (')[1:][0][:-1]
                        pageNum = math.ceil(int(count) / NUM_COUNT)
                        saveEntity = {
                            "url": url,
                            "page": pageNum,
                            "type1": oneLevelTypeName,
                            "type2": name,
                            "type3": "",
                            "count": int(count),
                            "createtime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                        }
                        print(">>> 信息正在入库 >>> ", saveEntity)
                        DBTool.DBTool().save_twoLevelData2mongoDB(saveEntity)
                    # 有子节点
                    for oneItem in oneDoc(".cate_has_child").items():
                        oneItemName = oneItem.text().split(' (')[0:1][0]
                        oneItemNew = oneItem.nextAll()
                        for twoItem in oneItemNew('.cate_child_name a').items():
                            url = SOGOU_MAIN_URL_BASE + twoItem.attr('href')
                            name = twoItem.text().split(' (')[0:1][0]
                            count = twoItem.text().split(' (')[1:][0][:-1]
                            pageNum = math.ceil(int(count) / NUM_COUNT)
                            saveEntity = {
                                "url": url,
                                "page": pageNum,
                                "type1": oneLevelTypeName,
                                "type2": oneItemName,
                                "type3": name,
                                "count": int(count),
                                "createtime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                            }
                            print(">>> 信息正在入库 >>> ", saveEntity)
                print(">>> 当前二级分类:", oneLevelTypeName, "信息获取结束!>>> ")
            print(">>> 获取二级分类数据所有的URL结束! >>>")
        except RequestException as e:
            print(">>> 获取二级分类数据所有的URL过程中发生异常, 请检查后重新获取! >>>")
            print(">>> 异常信息 >>>", e.strerror)

if __name__ == '__main__':
    # URLGrapMachine().get_one_level_url()
    URLGrapMachine().get_two_level_url()

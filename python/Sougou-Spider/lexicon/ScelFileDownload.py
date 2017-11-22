#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: ScelFileDownload.py

"""
Created on 2017/11/21 0021

@author: bigsea
"""

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import os
import urllib.request
import URLGrapTool
import DBTool
import multiprocessing

DIR_LIST = []
# 存放下载文件的目录
DIR = 'F:/PycharmProjects/Sougou-Spider/data/sougou'

"""
搜狗Scel文件下载器
"""
class FileDownloadMachine:
    def downloadFile(self, item):
        global DIR_LIST
        """
        分页请求下载搜狗页面scel文件
        :param item 单个对象
        :return: 
        """
        print(">>> 下载文件开始! >>>")
        url = item['url']
        page = item['page']
        type1 = item['type1']
        type2 = item['type2']
        type3 = item['type3']
        count = item['count']
        print(">>> 当前下载的词条分类：", type1, type2, type3, ">>>")
        print(">>> 共有", count, "个词库等待下载! >>>")
        try:
            # 计数器
            counte = 1
            while counte <= page:
                new_url = url + '/default/' + str(counte)
                response = requests.get(new_url)
                if response.status_code == requests.codes.ok:
                    html = response.text
                    soup = BeautifulSoup(html, "html.parser")
                    # 奇数部分
                    for detailItem in soup.select(".dict_detail_block"):
                        downloadDict = {
                            "type1": type1,
                            "type2": type2,
                            "type3": type3,
                            'fileName': detailItem.findAll("a")[0].string,
                            'fileHref': detailItem.findAll("a")[1]['href']
                        }
                        DIR_LIST.append(downloadDict)
                    # 偶数部分
                    for detailItem in soup.select(".dict_detail_block odd"):
                        downloadDict = {
                            "type1": type1,
                            "type2": type2,
                            "type3": type3,
                            'fileName': detailItem.findAll("a")[0].string,
                            'fileHref': detailItem.findAll("a")[1]['href']
                        }
                        DIR_LIST.append(downloadDict)
                    FileDownloadMachine().downloader()
                    DIR_LIST = []
                    counte = counte + 1
        except Exception as e:
            print(e)

    def downloader(self):
        global DIR_LIST
        """
        下载器
        :return: 
        """
        for dictItem in DIR_LIST:
            type1 = dictItem['type1']
            type2 = dictItem['type2']
            type3 = dictItem['type3']
            fileName = dictItem['fileName']
            fileHref = dictItem['fileHref']
            dest_dir = os.path.join(DIR, type1)
            if not os.path.exists(dest_dir):
                os.mkdir(dest_dir)
            dest_dir = os.path.join(dest_dir, type2)
            if not os.path.exists(dest_dir):
                os.mkdir(dest_dir)
            if type3 == "":
                pass
            else:
                dest_dir = os.path.join(dest_dir, type3)
                if not os.path.exists(dest_dir):
                    os.mkdir(dest_dir)
            file_dir = os.path.join(dest_dir, fileName + ".scel")
            try:
                print(">>>", type1, type2, type3, fileName, "文件开始下载, 下载地址:", fileHref, " >>>")
                urllib.request.urlretrieve(fileHref, file_dir)
                print(">>>", type1, type2, type3, fileName, "文件下载完成! >>>")
            except:
                print(">>>", type1, type2, type3, fileName, "文件下载异常! 下载地址:", fileHref, " >>>")
                error_content = ">>> " + type1 + " "+ type2 + " " + type3 + " "+ fileName + " 文件下载异常! 下载地址: " + fileHref + ">>>"
                file_name = "../" + '/file_error.txt'
                f = open(file_name, 'a')
                f.write(error_content + '\n')
                f.close()
                continue
        return

if __name__ == '__main__':
    twoLevelList = DBTool.DBTool().get_twoLevelData()
    if twoLevelList.count() == 0:
        URLGrapTool.URLGrapMachine().get_two_level_url()
    # 开线程
    count = twoLevelList.count()
    pool = multiprocessing.Pool(processes=100)
    for i in range(count):
        pool.apply_async(func=FileDownloadMachine().downloadFile, args=(twoLevelList[i],))
    pool.close()
    pool.join()
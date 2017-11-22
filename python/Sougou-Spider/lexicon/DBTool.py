#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: DBTool.py


"""
Created on 2017/11/21 0021

@author: bigsea
"""

from pymongo import MongoClient
"""
数据库工具
"""
class DBTool:
    __db__ = None
    __client__ = None
    __collection__ = None

    def __init__(self):
        # 建立 MongoDB 数据库连接
        self.__client__ = MongoClient('localhost', 27017)
        # 连接所需要的数据库, lexicon 为数据库的名称
        self.__db__ = self.__client__.lexicon_new

    def save_oneLevelData2mongoDB(self, data):
        """
        向 MongoDB 中插入所有一级分类数据
        :param data: 需要存储的数据
        :return: 
        """
        self.__collection__ = self.__db__.one_level
        self.__collection__.insert(data)

    def save_twoLevelData2mongoDB(self, data):
        """
        向 MongoDB 中插入所有二级分类数据
        :param data: 需要存储的数据
        :return: 
        """
        self.__collection__ = self.__db__.two_level
        self.__collection__.insert(data)

    def get_oneLevelData(self):
        """
        从 MongoDB 中查询出所有一级分类数据
        :return: 
        """
        self.__collection__ = self.__db__.one_level
        return self.__collection__.find()

    def get_twoLevelData(self):
        """
        从 MongoDB 中查询出所有二级分类数据
        :return: 
        """
        self.__collection__ = self.__db__.two_level
        return self.__collection__.find()
# -*- coding: utf-8 -*-

import pymongo

from parse_mooc_lec_json import read_lecture_info

def connect_db():
    my_client = pymongo.MongoClient("mongodb://super_sr:123456@209.97.166.185:27017/admin")
    my_db = my_client["sr_db1"]
    return my_db


def extract_comment_para():
    pass


def write_db():
    pass


def read_db():
    pass



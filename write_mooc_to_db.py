# -*- coding: utf-8 -*-

import pymongo

from parse_mooc_comments_json import read_comments_info, COMMENTS_DATA


def connect_db():
    client = pymongo.MongoClient("mongodb://super_sr:123456@209.97.166.185:27017/admin")
    db_opt = client["mooc_db_sr"]
    return db_opt


def write_db(dict_obj, db_opt):
    posts = db_opt['M' + str(dict_obj["lec_id"])]
    posts.insert(dict_obj)


def handle_db(comment_ls):
    db_opt = connect_db()
    for comment_dict in comment_ls:
        write_db(comment_dict, db_opt)


def read_db():
    db_opt = connect_db()
    collections_names = db_opt.collection_names()
    collections_names.remove('system.indexes')
    for collection in collections_names:
        print(next(db_opt[collection].find()))


if __name__ == '__main__':
    # comment_ls = read_comments_info(COMMENTS_DATA)
    # handle_db(comment_ls)
    read_db()

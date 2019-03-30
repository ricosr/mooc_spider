# -*- coding: utf-8 -*-

import pymongo

from parse_net_comments import combine_lec_comment, COMMENT_PICKLE, LECTURE_DATA


def connect_db():
    client = pymongo.MongoClient("mongodb://xxx:xxxxxx@209.97.xxx.xxx:27017/admin")
    db_opt = client["net_db_sr"]
    return db_opt


def write_db(dict_obj, db_opt):
    posts = db_opt['N' + str(dict_obj["lec_id"])]
    posts.insert(dict_obj)


def handle_db(comments_dict):
    db_opt = connect_db()
    for lec_id, comment_dict in comments_dict.items():
        write_db(comment_dict, db_opt)


def read_db():
    db_opt = connect_db()
    collections_names = db_opt.collection_names()
    collections_names.remove('system.indexes')
    for collection in collections_names[:1]:
        print(next(db_opt[collection].find()))


if __name__ == '__main__':
    comments_dict = combine_lec_comment(LECTURE_DATA, COMMENT_PICKLE)
    handle_db(comments_dict)
    # read_db()

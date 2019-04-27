# -*- coding: utf-8 -*-

import pickle

COMMENT_PICKLE = "net_data/lecture_comments"
LECTURE_DATA = "net_data/lectures_data.pkl"


def read_net_comment_pickles(pickles_path):
    with open(pickles_path, "rb") as pwf:
        comments_data = pickle.load(pwf)
    return comments_data


def read_net_lec_data(lec_data_path):
    with open(lec_data_path, "rb") as pwf:
        lecture_data = pickle.load(pwf)
    return lecture_data


def combine_lec_comment(lec_data_path, comment_path):
    lecture_data = read_net_lec_data(lec_data_path)
    lec_id_ls = list(lecture_data.keys())
    for lec_id in lec_id_ls:
        comment_pkl_path = "{}/{}.pkl".format(comment_path, str(lec_id))
        comments = read_net_comment_pickles(comment_pkl_path)
        lecture_data[lec_id]["comments"] = comments
    return lecture_data

# combine_lec_comment(LECTURE_DATA, COMMENT_PICKLE)



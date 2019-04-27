# -*- coding: utf-8 -*-

# extract comments info from json files

import json
import pickle
import copy


from parse_mooc_lec_json import read_lecture_info, LECTURE_DATA, Teacher, Lecture


COMMENTS_DATA = "mooc_data/comments_data.pkl"
COMMENTS_JSON = "mooc_data/lecture_comments"


def read_json_file(json_file_path):    # 2
    comments_ls = []
    with open(json_file_path, 'r', encoding='utf-8') as fpr:
        json_ls = fpr.readlines()
    for each_json in json_ls:
        comments_ls.extend(json.loads(each_json)["result"]["list"])
    return comments_ls


def save_comments_data(pickle_path, content):     # 4
    with open(pickle_path, 'wb') as fpw:
        pickle.dump(content, fpw)


def get_comments_info(comments_ls):    # 3
    comment_para_ls = []
    for comment in comments_ls:
        tmp_dict = {}
        tmp_dict["content"] = comment["content"]
        tmp_dict["mark"] = comment["mark"]
        tmp_dict["agreeCount"] = comment["agreeCount"]
        comment_para_ls.append(tmp_dict)
    return comment_para_ls


def handle_mooc_comment(comment_json_path, lecture_data_path):    # 1
    lectures_ls = read_lecture_info(lecture_data_path)
    result_ls = copy.deepcopy(lectures_ls)
    for i in range(len(lectures_ls)):
        lecture = lectures_ls[i]
        lec_id = lecture["lec_id"]
        json_file_path = "{}/{}.json".format(comment_json_path, str(lec_id))
        tmp_comments_ls = read_json_file(json_file_path)
        comments_ls = get_comments_info(tmp_comments_ls)
        result_ls[i]["comments"] = comments_ls
    return result_ls


def read_comments_info(pickle_path):    # 5
    with open(pickle_path, "rb") as pwf:
        content = pickle.load(pwf)
    return content

if __name__ == '__main__':
    result = handle_mooc_comment(COMMENTS_JSON, LECTURE_DATA)
    save_comments_data(COMMENTS_DATA, result)
    # content = read_comments_info(COMMENTS_DATA)





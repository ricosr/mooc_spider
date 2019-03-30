# -*- coding: utf-8 -*-

# extract lecture info from json files

import json
import pickle
import os


LECTURE_DATA = "net_data/lectures_data.pkl"
LECTURE_JSON = "net_data/net_url"


def read_json_file(json_path):   # return a dictionary result object
    with open(json_path, 'r', encoding='utf-8') as fpr:
        dict_data = json.load(fpr)
    return dict_data["result"]["list"]


def save_lecture_data(lec_info, lecture_data_path):
    with open(lecture_data_path, 'wb') as fpw:
        pickle.dump(lec_info, fpw)


def get_lec_info(result_obj):
    tmp_lec_dict = {}
    for each_obj in result_obj:
        lec_info_dict = {}
        product_id = each_obj["productId"]
        lec_info_dict["lec_id"] = each_obj["courseId"]
        if product_id != lec_info_dict["lec_id"]:
            continue

        lec_info_dict["lec_name"] = each_obj["productName"]

        lec_info_dict["learner_count"] = each_obj["learnerCount"]
        lec_info_dict["lesson_count"] = each_obj["lessonCount"]

        provider = each_obj["provider"]
        lector_name = each_obj["lectorName"]
        if not lector_name:
            lector_name = provider
        lec_info_dict["lec_name"] = lector_name

        lec_info_dict["school_name"] = provider
        lec_info_dict["school_short_name"] = ''

        if each_obj["vipContentType"] == 1:
            vip = "vip_discount"
        else:
            vip = None
        lec_info_dict["vip"] = vip

        lec_info_dict["score"] = each_obj["score"]
        lec_info_dict["score_level"] = each_obj["scoreLevel"]

        lec_info_dict["img_url"] = each_obj["imgUrl"]
        lec_info_dict["description"] = each_obj["description"]
        tmp_lec_dict[product_id] = lec_info_dict
    return tmp_lec_dict


def handle_net_lecture(json_path, lecture_data_path):
    all_lec_dict = {}
    for file_name in os.listdir(json_path):
        each_file_path = os.path.join(json_path, file_name)
        # print(each_file_path)
        result_obj = read_json_file(each_file_path)
        temp_lec_info = get_lec_info(result_obj)
        all_lec_dict.update(temp_lec_info)
    save_lecture_data(all_lec_dict, lecture_data_path)

if __name__ == '__main__':
    handle_net_lecture(LECTURE_JSON, LECTURE_DATA)
# temp = read_lecture_info()
# print(temp)

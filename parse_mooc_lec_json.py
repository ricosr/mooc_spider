# -*- coding: utf-8 -*-

# extract lecture info from json files

import json
import pickle
import os


LECTURE_DATA = "mooc_data/lectures_data.pkl"


class Teacher:
    def __init__(self, real_name, lector_title):
        self.real_name = real_name
        self.lector_title = lector_title


class Lecture:
    def __init__(self, lec_id, lec_name, school_name, school_short_name, moc_tag_dtos):
        self.lec_id = lec_id
        self.lec_name = lec_name
        self.school_name = school_name
        self.school_short_name = school_short_name
        self.moc_tag_dtos = moc_tag_dtos
        self.teacher_info = []

    def get_teachers_info(self, teacher_ls):
        for each_teacher in teacher_ls:
            tmp_name = each_teacher["realName"]
            tmp_title = each_teacher["lectorTitle"]
            teacher = Teacher(tmp_name, tmp_title)
            self.teacher_info.append(teacher)


def read_json_file(json_path):   # return a dictionary result object
    with open(json_path, 'r', encoding='utf-8') as fpr:
        dict_data = json.load(fpr)
    return dict_data["result"]["result"]


def save_lecture_data(lec_info):
    global LECTURE_DATA
    with open(LECTURE_DATA, 'wb') as fpw:
        pickle.dump(lec_info, fpw)


def get_lec_info(result_obj):
    lec_info_dict = {}
    for each_obj in result_obj:
        lec_id = each_obj["id"]
        lec_name = each_obj["name"]
        school_name = each_obj["schoolPanel"]["name"]
        school_short_name = each_obj["schoolPanel"]["shortName"]
        moc_tag_dtos = ''
        if each_obj["mocTagDtos"]:
            tmp_moc = each_obj["mocTagDtos"][0]
            if "name" in tmp_moc:
                moc_tag_dtos += tmp_moc["name"] + ','
            if "comment" in tmp_moc:
                moc_tag_dtos += tmp_moc["comment"]
        lecture_obj = Lecture(lec_id, lec_name, school_name, school_short_name, moc_tag_dtos)
        lecture_obj.get_teachers_info(each_obj["termPanel"]["lectorPanels"])
        lec_info_dict[lec_id] = lecture_obj
        # print(lec_info_ls)
    return lec_info_dict


def handle_mooc_lecture(json_path):
    all_lec_dict = {}
    for file_name in os.listdir(json_path):
        each_file_path = os.path.join(json_path, file_name)
        result_obj = read_json_file(each_file_path)
        temp_lec_info = get_lec_info(result_obj)
        all_lec_dict.update(temp_lec_info)
    save_lecture_data(all_lec_dict)


def tmp_test():
    global LECTURE_DATA
    with open(LECTURE_DATA, "rb") as pwf:
        content = pickle.load(pwf)
    print(len(content))
    count = 0
    for lec_id, each_lec in content.items():
        print(count)
        print(each_lec.lec_id)
        print(each_lec.lec_name)
        print(each_lec.school_name)
        print(each_lec.school_short_name)
        print(each_lec.moc_tag_dtos)
        print()
        for teacher in each_lec.teacher_info:
            print(teacher.real_name)
            print(teacher.lector_title)
            print('***************')
        print('-----------------------------------------------')
        count += 1


# handle_mooc_lecture("mooc_data/mooc_url")
# tmp_test()

# -*- coding: utf-8 -*-

import json
import pickle
import os


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
    with open("mooc_data/lectures_data.pkl", 'wb') as fpw:
        pickle.dump(lec_info, fpw)


def get_lec_info(result_obj):
    lec_info_ls = []
    for each_obj in result_obj:
        lec_id = each_obj["id"]
        lec_name = each_obj["name"]
        school_name = each_obj["schoolPanel"]["name"]
        school_short_name = each_obj["schoolPanel"]["shortName"]
        moc_tag_dtos = ''
        if each_obj["mocTagDtos"]:
            tmp_moc = each_obj["mocTagDtos"]
            if "name" in tmp_moc:
                moc_tag_dtos += tmp_moc["name"]
            if "comment" in tmp_moc:
                moc_tag_dtos += tmp_moc["comment"]
        lecture_obj = Lecture(lec_id, lec_name, school_name, school_short_name, moc_tag_dtos)
        lecture_obj.get_teachers_info(each_obj["termPanel"]["lectorPanels"])
        lec_info_ls.append(lecture_obj)
        print(lec_info_ls)
    save_lecture_data(lec_info_ls)


def handle_mooc_lecture(json_path):
    for file_name in os.listdir(json_path):
        each_file_path = os.path.join(json_path, file_name)
        result_obj = read_json_file(each_file_path)
        get_lec_info(result_obj)

handle_mooc_lecture("mooc_data/mooc_url")
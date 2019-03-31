# -*- coding: utf-8 -*-

# extract lecture info from json files

import json
import pickle
import os


LECTURE_DATA = "mooc_data/lectures_data.pkl"
LECTURE_JSON = "mooc_data/mooc_url"


class Teacher:
    def __init__(self, real_name, lector_title):
        self.real_name = real_name
        self.lector_title = lector_title


class Lecture:
    def __init__(self, lec_id, lec_name, school_name, school_short_name, moc_tag_dtos, img_url):
        self.lec_id = lec_id
        self.lec_name = lec_name
        self.school_name = school_name
        self.school_short_name = school_short_name
        self.moc_tag_dtos = moc_tag_dtos
        self.img_url = img_url
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


def save_lecture_data(lec_info, lecture_data_path):
    with open(lecture_data_path, 'wb') as fpw:
        pickle.dump(lec_info, fpw)


def get_lec_info(result_obj):
    lec_info_dict = {}
    for each_obj in result_obj:
        lec_id = each_obj["id"]
        lec_name = each_obj["name"]
        img_url = each_obj["imgUrl"]
        school_name = each_obj["schoolPanel"]["name"]
        school_short_name = each_obj["schoolPanel"]["shortName"]
        moc_tag_dtos = ''
        if each_obj["mocTagDtos"]:
            tmp_moc = each_obj["mocTagDtos"][0]
            if "name" in tmp_moc:
                moc_tag_dtos += tmp_moc["name"] + ','
            if "comment" in tmp_moc:
                moc_tag_dtos += tmp_moc["comment"]
        lecture_obj = Lecture(lec_id, lec_name, school_name, school_short_name, moc_tag_dtos, img_url)
        lecture_obj.get_teachers_info(each_obj["termPanel"]["lectorPanels"])
        lec_info_dict[lec_id] = lecture_obj
    return lec_info_dict


def handle_mooc_lecture(json_path, lecture_data_path):
    all_lec_dict = {}
    for file_name in os.listdir(json_path):
        each_file_path = os.path.join(json_path, file_name)
        result_obj = read_json_file(each_file_path)
        temp_lec_info = get_lec_info(result_obj)
        all_lec_dict.update(temp_lec_info)
    save_lecture_data(all_lec_dict, lecture_data_path)


def read_lecture_info(lecture_data_path):
    lectures_ls = []
    with open(lecture_data_path, "rb") as pwf:
        content = pickle.load(pwf)
    for lec_id, each_lec in content.items():
        tmp_lec_dict = {}
        tmp_lec_dict["lec_id"] = each_lec.lec_id
        tmp_lec_dict["lec_name"] = each_lec.lec_name
        tmp_lec_dict["school_name"] = each_lec.school_name
        tmp_lec_dict["school_short_name"] = each_lec.school_short_name
        tmp_lec_dict["moc_tag_dtos"] = each_lec.moc_tag_dtos
        tmp_lec_dict["img_url"] = each_lec.img_url
        tmp_teacher_dict = {}
        for teacher in each_lec.teacher_info:
            if teacher.real_name:
                tmp_teacher_dict[teacher.real_name] = teacher.lector_title
        tmp_lec_dict["teachers"] = tmp_teacher_dict
        lectures_ls.append(tmp_lec_dict)
    return lectures_ls


if __name__ == '__main__':
    handle_mooc_lecture(LECTURE_JSON, LECTURE_DATA)


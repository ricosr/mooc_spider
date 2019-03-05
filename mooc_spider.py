# -*- coding: utf-8 -*-

import json

import requests


def do_post(url, cookie, data):
    try:
        headers = {
                   "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Language": "en-us",
                   "Connection": "keep-alive",
                   "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7",
                   "cookie": cookie
        }
        response = requests.post(url, data, headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except Exception as e:
        print(e)


def get_lectures_urls(html):
    pass


def get_comment_content():
    pass


def save_comment():
    pass


def judge_null(json_data):
    py_data = json.loads(json_data)
    if py_data["result"]["result"] == None:
        return True


def save_data(json_data, path):
    with open(path, 'w', encoding='utf-8') as fpr:
        fpr.write(json_data)



def get_lec_ids(lec_type_no):
    URL = "https://www.icourse163.org/web/j/courseBean.getCoursePanelListByFrontCategory.rpc?csrfKey=f9410e1214a6417690642ec43ac39a84"
    cookie = "EDUWEBDEVICE=a32f0ffb30ed4f0f878f567ebf5d7c30; hb_MA-A976-948FFA05E931_source=www.google.com; WM_NI=%2Fkb3Anlp6vVqZkDILsGLg%2BCwSHazM9hAUYix3BnKYODc8Q5X6Y3v92WIUfMlGlBrA7U9XMqRPHmjbafoQgy%2F8BCzC%2BS8Dmb8aLRb8SZd8%2BhZHok%2BVh3DLnj8WZqWOZmZN0Y%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed2d749b396a384f94b82ac8aa3c45a868b9fbaee6dac95fc87d55e8e88bd84c52af0fea7c3b92aedb5aed4c466b0b0fa97d57b9ab58caacf798594a9ccc27d9198af9bd033ac9f9bbaec74f19ea2acdc4588bdf8b2b854f687fd97bc3a95979b87d06885b48e93c43d97e798aef45a9498a38be16ba6b19f88fc25fc9e8d9bc22191e88c8ee134a3949e83bb599abcf8cceb528cb1a5ccd564f19c848fe9349586bfb8ce52af8682d1dc37e2a3; WM_TID=opyJCGkLpOlEERQFRUJ4llLsaBAcT9cU; __utmz=63145271.1551009411.4.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utma=63145271.661424980.1550992805.1551012464.1551058586.6; __utmc=63145271; NTESSTUDYSI=f9410e1214a6417690642ec43ac39a84; __utmb=63145271.14.9.1551059375768"
    count = 1
    while True:
        data = {
            "categoryId": "{}".format(lec_type_no),    # "1001043131",
            "type": "30",
            "orderBy": "0",
            "pageIndex": "{}".format(count),
            "pageSize": "20"
        }
        json_data = do_post(URL, cookie, data)
        if judge_null(json_data):
            break
        save_data(json_data, "mooc_data/mooc_url/computer_page_{}.json".format(count))
        count += 1

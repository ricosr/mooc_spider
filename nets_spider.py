# -*- coding: utf-8 -*-

import json

import requests


def get_response_json(url, cookie, data):
    try:
        # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
        #            "Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #            "Accept-Language": "en-us",
        #            "Connection": "keep-alive",
        #            "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7",
        #            "cookie": cookie
        #            }
        headers = {
            "authority": "study.163.com",
            "method": "POST",
            "path": "/p/search/studycourse.json",
            "scheme": "https",
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN, zh;q = 0.9",
            "content-length": "162",
            "content-type": "application/json",
            "cookie": cookie,
            "edu-script-token": "a428291b5655402c9251ee7ff6b9ff2f",
            "origin": "https://study.163.com",
            "referer": "https://study.163.com/category/480000003121007",
            "user-agent": "Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 69.0.3497.92 Safari / 537.36"
        }
        response = requests.post(url, json.dumps(data), headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except Exception as e:
        print(e)


def get_lectures_urls():
    pass


def get_comment_content():
    pass


def save_comment():
    pass


def save_data(json_data, path):
    with open(path, 'w', encoding='utf-8') as fpr:
        fpr.write(json_data)


if __name__ == '__main__':
    URL = "https://study.163.com/p/search/studycourse.json"
    cookie = "usertrack=CrHuaVxnc/u07+fAAy54Ag==; _ntes_nnid=daaa9fcf449d023308cf75dd9723a92c,1550283771180; _ntes_nuid=daaa9fcf449d023398cf75dd9723a92c; P_INFO=ricosr@163.com|1550497883|0|other|00&99|hongkong&1550496512&mail_client#hongkong&810000#10#0#0|&0|youdaodict_client|ricosr@163.com; mail_psc_fingerprint=35dd15f189a94ebd1d0f0fea63ded83c; EDUWEBDEVICE=63d891ba96bc4407ac77d75669dff188; __utmz=129633230.1550990328.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); NTESSTUDYSI=a428291b5655402c9251ee7ff6b9ff2f; __utma=129633230.1904989255.1550990328.1551058647.1551075098.7; __utmc=129633230; STUDY_UUID=ae9c594e-2c92-452b-a12a-f431e4c0f150; utm=eyJjIjoiIiwiY3QiOiIiLCJpIjoiIiwibSI6IiIsInMiOiIiLCJ0IjoiIn0=|aHR0cHM6Ly9zdHVkeS4xNjMuY29tL2NhdGVnb3J5LzQ4MDAwMDAwMzEyMTAwNw==; __utmb=129633230.98.9.1551085437256"
    key_words_ls = ["Python", "数据挖掘", "Java", "C语言", "前端开发", "IOS", "数据分析", "人工智能", "大数据", "大数据", "区块链"]
    # "Python", "数据挖掘", "Java", "C语言", "前端开发", "IOS", "数据分析", "人工智能", "大数据", "大数据", "区块链"
    for key_word in key_words_ls:
        count = 1
        while True:
            data = {
                        "pageIndex": "{}".format(count),
                        "pageSize": 50,
                        "relativeOffset": 0,
                        "keyword": key_word,
                        "searchTimeType": -1,
                        "orderType": 50,
                        "priceType": -1,
                        "activityId": 0,
                        "qualityType": 0
            }

            json_content = get_response_json(URL, cookie, data)
            if not json.loads(json_content)["result"]["list"]:
                break
            save_data(json_content, "net_data/net_url/{}_page_{}.json".format(key_word, count))
            count += 1


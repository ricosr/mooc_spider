# -*- coding: utf-8 -*-

import json

import requests


def get_page_html(url, cookie, data):
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


if __name__ == '__main__':
    # URL = "https://study.163.com/dwr/call/plaincall/CourseBean.getMixCourseCardDto.dwr?1551060448677"
    URL = "https://study.163.com/p/search/studycourse.json"
    # cookie = "usertrack=CrHuaVxnc/u07+fAAy54Ag==; _ntes_nnid=daaa9fcf449d023398cf75dd9723a92c,1550283771180; _ntes_nuid=daaa9fcf449d023398cf75dd9723a92c; P_INFO=ricosr@163.com|1550497883|0|other|00&99|hongkong&1550496512&mail_client#hongkong&810000#10#0#0|&0|youdaodict_client|ricosr@163.com; mail_psc_fingerprint=35dd15f189a94ebd1d0f0fea63ded83c; EDUWEBDEVICE=63d891ba96bc4407ac77d75669dff188; __utmz=129633230.1550990328.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); NTESSTUDYSI=3fd3f9fbe2ad4ba1a317ab04b664490d; __utma=129633230.1904989255.1550990328.1551015528.1551058647.6; __utmc=129633230; __utmb=129633230.13.9.1551059456551"
    cookie = "usertrack=CrHuaVxnc/u07+fAAy54Ag==; _ntes_nnid=daaa9fcf449d023308cf75dd9723a92c,1550283771180; _ntes_nuid=daaa9fcf449d023398cf75dd9723a92c; P_INFO=ricosr@163.com|1550497883|0|other|00&99|hongkong&1550496512&mail_client#hongkong&810000#10#0#0|&0|youdaodict_client|ricosr@163.com; mail_psc_fingerprint=35dd15f189a94ebd1d0f0fea63ded83c; EDUWEBDEVICE=63d891ba96bc4407ac77d75669dff188; __utmz=129633230.1550990328.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); NTESSTUDYSI=a428291b5655402c9251ee7ff6b9ff2f; __utma=129633230.1904989255.1550990328.1551058647.1551075098.7; __utmc=129633230; STUDY_UUID=ae9c594e-2c92-452b-a12a-f431e4c0f150; utm=eyJjIjoiIiwiY3QiOiIiLCJpIjoiIiwibSI6IiIsInMiOiIiLCJ0IjoiIn0=|aHR0cHM6Ly9zdHVkeS4xNjMuY29tL2NhdGVnb3J5LzQ4MDAwMDAwMzEyMTAwNw==; __utmb=129633230.98.9.1551085437256"
    # data = {
    #     "callCount": "1",
    #     "scriptSessionId": "${scriptSessionId}190",
    #     "httpSessionId": "3fd3f9fbe2ad4ba1a317ab04b664490d",
    #     "c0-scriptName": "CourseBean",
    #     "c0-methodName": "getMixCourseCardDto",
    #     "c0-id": "0",
    #     "c0-e1": "number:4000",
    #     "c0-e2": "number:0",
    #     "c0-e3": "string:480000003121007",
    #     "c0-e4": "number:0",
    #     "c0-e5": "number:0",
    #     "c0-param0": "Object_Object:{size:reference:c0-e1,index:reference:c0-e2,frontCategoryId:reference:c0-e3,timeType:reference:c0-e4,orderBy:reference:c0-e5}",
    #     "batchId": "1551060448577"
    # }
    data = {"pageIndex": "1",
            "pageSize": "50",
            "relativeOffset": "0",
            "frontCategoryId": "480000003121007",
            "searchTimeType": "-1",
            "orderType": "50",
            "priceType": "-1",
            "activityId": "0",
            "advertiseSearchUuid": "634252e4-ac1b-46e9-9912-9362bf1a2340",
            "keyword": ""
            }

    html_content = get_page_html(URL, cookie, data)
    print(html_content)
    with open("log.txt", 'a', encoding='utf-8') as fw:
        fw.write(html_content)
    # if "7028" in html_content:
    #     print("done!")

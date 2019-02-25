# -*- coding: utf-8 -*-

import requests


def get_page_html(url, cookie, data):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
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


def get_lectures_urls():
    pass


def get_comment_content():
    pass


def save_comment():
    pass


if __name__ == '__main__':
    URL = "https://study.163.com/dwr/call/plaincall/CourseBean.getMixCourseCardDto.dwr?1551060448677"
    cookie = "usertrack=CrHuaVxnc/u07+fAAy54Ag==; _ntes_nnid=daaa9fcf449d023398cf75dd9723a92c,1550283771180; _ntes_nuid=daaa9fcf449d023398cf75dd9723a92c; P_INFO=ricosr@163.com|1550497883|0|other|00&99|hongkong&1550496512&mail_client#hongkong&810000#10#0#0|&0|youdaodict_client|ricosr@163.com; mail_psc_fingerprint=35dd15f189a94ebd1d0f0fea63ded83c; EDUWEBDEVICE=63d891ba96bc4407ac77d75669dff188; __utmz=129633230.1550990328.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); NTESSTUDYSI=3fd3f9fbe2ad4ba1a317ab04b664490d; __utma=129633230.1904989255.1550990328.1551015528.1551058647.6; __utmc=129633230; __utmb=129633230.13.9.1551059456551"
    data = {
        "callCount":"1",
        "scriptSessionId":"${scriptSessionId}190",
        "httpSessionId":"3fd3f9fbe2ad4ba1a317ab04b664490d",
        "c0-scriptName":"CourseBean",
        "c0-methodName":"getMixCourseCardDto",
        "c0-id":"0",
        "c0-e1":"number:10",
        "c0-e2":"number:1",
        "c0-e3":"string:480000003121007",
        "c0-e4":"number:30",
        "c0-e5":"number:60",
        "c0-param0":"Object_Object:{size:reference:c0-e1,index:reference:c0-e2,frontCategoryId:reference:c0-e3,timeType:reference:c0-e4,orderBy:reference:c0-e5}",
        "batchId":"1551060448577"
    }
    html_content = get_page_html(URL, cookie, data)
    print(html_content)

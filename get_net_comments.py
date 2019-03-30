# -*- coding: utf-8 -*-

# download comments from all lectures

import pickle
import threading
import traceback

import requests

COMMENT_PICKLE = "net_data/lecture_comments"
LECTURE_DATA = "net_data/lectures_data.pkl"


def read_lec_data(lec_data_path):
    with open(LECTURE_DATA, "rb") as pwf:
        content = pickle.load(pwf)
    lec_id_ls = list(content.keys())
    return lec_id_ls


def save_comments_data(pickle_path, content):
    with open(pickle_path, 'wb') as fpw:
        pickle.dump(content, fpw)


def parse_comments_response(response_content):
    data_ls = response_content.split('\n')
    total_page_count_index = 0
    total_page_count = 0
    comment_list = []
    for each in data_ls:
        if "totlePageCount" in each:
            total_page_count_index = data_ls.index(each)
            tmp_line_ls = each.split(';')
            for element in tmp_line_ls:
                if "totlePageCount" in element:
                    total_page_count = element.split('=')[1]
                    break
            break
    for each_line in data_ls[total_page_count_index+2:-2]:
        each_line_ls = each_line.split(';')
        tmp_comment_dict = {}
        try:
            for element in each_line_ls:
                if "content=" in element:
                    tmp_comment_dict["content"] = element.split('=')[1].strip('\"').encode("GBK").decode("unicode-escape")
                if "mark=" in element:
                    tmp_comment_dict["mark"] = float(element.split('=')[1])
                if "replyContent=" in element:
                    tmp_comment_dict["reply"] = element.split('=')[1].strip('\"').encode("utf-8").decode("unicode-escape")
            if tmp_comment_dict:
                comment_list.append(tmp_comment_dict)
        except Exception as e:
            print('traceback.format_exc():\n%s' % traceback.format_exc())

    return comment_list, int(total_page_count)


def request_lec_comments(courseId, pickle_path):
    all_comments_list = []
    url = "https://study.163.com/dwr/call/plaincall/AskCommentBean.getOnePageComment.dwr"
    cookie = "usertrack=CrHuaVxnc/u07+fAAy54Ag==; _ntes_nnid=daaa9fcf449d023398cf75dd9723a92c,1550283771180; _ntes_nuid=daaa9fcf449d023398cf75dd9723a92c; P_INFO=ricosr@163.com|1550497883|0|other|00&99|hongkong&1550496512&mail_client#hongkong&810000#10#0#0|&0|youdaodict_client|ricosr@163.com; mail_psc_fingerprint=35dd15f189a94ebd1d0f0fea63ded83c; NTESSTUDYSI=49cd2e37570f45a6b4761c1ec5fc96fd; EDUWEBDEVICE=63d891ba96bc4407ac77d75669dff188; __utmc=129633230; __utmz=129633230.1550990328.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); STUDY_UUID=a9513a51-a170-4f7b-86ea-f2fa1c73b574; utm=eyJjIjoiIiwiY3QiOiIiLCJpIjoiIiwibSI6IiIsInMiOiIiLCJ0IjoiIn0=|aHR0cHM6Ly9zdHVkeS4xNjMuY29tL2NvdXJzZS9pbnRyb2R1Y3Rpb24vMTAwNTY4MDAxMS5odG0=; __utma=129633230.1904989255.1550990328.1550990328.1550997685.2; __utmb=129633230.3.8.1550997688164"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-us",
        "Connection": "keep-alive",
        "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7",
        "cookie": cookie
    }
    data = {
        'callCount': '1',
        'scriptSessionId': '${scriptSessionId}190',
        'httpSessionId': '49cd2e37570f45a6b4761c1ec5fc96fd',
        'c0-scriptName': 'AskCommentBean',
        'c0-methodName': 'getOnePageComment',
        'c0-id': '0',
        'c0-param0': 'string:{}'.format(courseId),
        'c0-param1': 'number:30',
        'c0-param2': 'number:1',
        'batchId': '1550997687681'
    }
    response = requests.post(url, data, headers=headers)
    comment_list, total_page_count = parse_comments_response(response.text)
    all_comments_list.extend(comment_list)

    if total_page_count > 1:
        for page_count in range(2, total_page_count+1):
            data = {
                'callCount': '1',
                'scriptSessionId': '${scriptSessionId}190',
                'httpSessionId': '49cd2e37570f45a6b4761c1ec5fc96fd',
                'c0-scriptName': 'AskCommentBean',
                'c0-methodName': 'getOnePageComment',
                'c0-id': '0',
                'c0-param0': 'string:{}'.format(courseId),  # 1003852044
                'c0-param1': 'number:30',
                'c0-param2': 'number:{}'.format(str(page_count)),
                'batchId': '1550997687681'
            }
            response = requests.post(url, data, headers=headers)
            comment_list, total_page_count = parse_comments_response(response.text)
            all_comments_list.extend(comment_list)
    save_path = "{}/{}.pkl".format(pickle_path, courseId)
    # print(all_comments_list)
    save_comments_data(save_path, all_comments_list)


def mul_thread_crawl(threading_num, block_ls, pickle_path):
    def download_fun(course_id_ls):
        for course_id in course_id_ls:
            request_lec_comments(course_id, pickle_path)
    thread_ls = []
    for i in range(threading_num):
        thread_ls.append(threading.Thread(target=download_fun, args=(block_ls[i],)))
    for i in range(threading_num):
        thread_ls[i].start()


def test(block_count):
    global LECTURE_DATA
    global COMMENT_PICKLE
    lec_id_ls = read_lec_data(LECTURE_DATA)
    if len(lec_id_ls) > block_count:
        block_size = len(lec_id_ls) // block_count
        block_ls = []

        start_index = 0
        for i in range(block_count):
            block_ls.append(lec_id_ls[start_index:start_index+block_size])
            start_index = start_index + block_size
        if start_index < len(lec_id_ls):
            block_ls.append(lec_id_ls[start_index:])
        threading_num = len(block_ls)
        mul_thread_crawl(threading_num, block_ls, COMMENT_PICKLE)
    else:
        for lec_id in lec_id_ls:
            request_lec_comments(lec_id, COMMENT_PICKLE)

# request_lec_comments("1003852044", COMMENT_PICKLE)

test(5)

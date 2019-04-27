import requests

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
        'c0-param0': 'string:1003852044',
        'c0-param1': 'number:30',
        'c0-param2': 'number:3',
        'batchId': '1550997687681'
    }

response = requests.post(url, data, headers=headers)

# var s0=[];var s3={};var s4={};var s5={};var s6={};var s1={};var s2=[];var s7={};var s27={};var s8={};var s28={};var s9={};var s29={};var s10={};var s30={};var s11={};var s31={};var s12={};var s32={};var s13={};var s33={};var s14={};var s34={};var s15={};var s35={};var s16={};var s36={};var s17={};var s37={};var s18={};var s38={};var s19={};var s39={};var s20={};var s40={};var s21={};var s41={};var s22={};var s42={};var s23={};var s43={};var s24={};var s44={};var s25={};var s45={};var s26={};var s46={};s0[0]=s3;s0[1]=s4;s0[2]=s5;s0[3]=s6;
# s3.count=1;s3.mark=2.0;
# s4.count=1;s4.mark=3.0;
# s5.count=3;s5.mark=4.0;
# s6.count=35;s6.mark=5.0;
# s1.limit=20;s1.offset=0;s1.pageIndex=1;s1.pageSize=20;s1.sortCriterial="score desc, gmt_create desc";s1.totleCount=40;s1.totlePageCount=2;

# page count: s1.totlePageCount=2;

print(len(response.text.split('\n')))

# import random
# d1 = {}
# for i in range(10):
#     d = {}
#     d[i] = i*random.randint(1, 100)
#     d1[i] = d
#
# print(d1)

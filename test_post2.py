import requests

url = "https://study.163.com/dwr/call/plaincall/AskCommentBean.getOnePageComment.dwr"

cookie = "usertrack=CrHuaVxnc/u07+fAAy54Ag==; _ntes_nnid=daaa9fcf449d023398cf75dd9723a92c,1550283771180; _ntes_nuid=daaa9fcf449d023398cf75dd9723a92c; P_INFO=ricosr@163.com|1550497883|0|other|00&99|hongkong&1550496512&mail_client#hongkong&810000#10#0#0|&0|youdaodict_client|ricosr@163.com; mail_psc_fingerprint=35dd15f189a94ebd1d0f0fea63ded83c; NTESSTUDYSI=49cd2e37570f45a6b4761c1ec5fc96fd; EDUWEBDEVICE=63d891ba96bc4407ac77d75669dff188; __utmc=129633230; __utmz=129633230.1550990328.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); STUDY_UUID=a9513a51-a170-4f7b-86ea-f2fa1c73b574; utm=eyJjIjoiIiwiY3QiOiIiLCJpIjoiIiwibSI6IiIsInMiOiIiLCJ0IjoiIn0=|aHR0cHM6Ly9zdHVkeS4xNjMuY29tL2NvdXJzZS9pbnRyb2R1Y3Rpb24vMTAwNTY4MDAxMS5odG0=; __utma=129633230.1904989255.1550990328.1550990328.1550997685.2; __utmb=129633230.3.8.1550997688164"

headers={"User-Agent" : "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
  "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  "Accept-Language" : "en-us",
  "Connection" : "keep-alive",
  "Accept-Charset" : "GB2312,utf-8;q=0.7,*;q=0.7",
  "cookie": cookie
}

data = {
    'callCount':'1',
    'scriptSessionId':'${scriptSessionId}190',
    'httpSessionId':'49cd2e37570f45a6b4761c1ec5fc96fd',
    'c0-scriptName':'AskCommentBean',
    'c0-methodName':'getOnePageComment',
    'c0-id':'0',
    'c0-param0':'string:1003852044',
    'c0-param1':'number:30',
    'c0-param2':'number:1',
    'batchId':'1550997687681'
}

response = requests.post(url, data, headers=headers)

print(response.text)
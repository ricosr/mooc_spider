import requests

url = "https://www.icourse163.org/web/j/mocCourseV2RpcBean.getCourseEvaluatePaginationByCourseIdOrTermId.rpc?csrfKey=d716f7686cf944cbbffa1977e7739221"

cookie = "NTESSTUDYSI=d716f7686cf944cbbffa1977e7739221; EDUWEBDEVICE=a32f0ffb30ed4f0f878f567ebf5d7c30; hb_MA-A976-948FFA05E931_source=www.google.com; __utmc=63145271; __utmz=63145271.1550992805.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); WM_NI=%2Fkb3Anlp6vVqZkDILsGLg%2BCwSHazM9hAUYix3BnKYODc8Q5X6Y3v92WIUfMlGlBrA7U9XMqRPHmjbafoQgy%2F8BCzC%2BS8Dmb8aLRb8SZd8%2BhZHok%2BVh3DLnj8WZqWOZmZN0Y%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed2d749b396a384f94b82ac8aa3c45a868b9fbaee6dac95fc87d55e8e88bd84c52af0fea7c3b92aedb5aed4c466b0b0fa97d57b9ab58caacf798594a9ccc27d9198af9bd033ac9f9bbaec74f19ea2acdc4588bdf8b2b854f687fd97bc3a95979b87d06885b48e93c43d97e798aef45a9498a38be16ba6b19f88fc25fc9e8d9bc22191e88c8ee134a3949e83bb599abcf8cceb528cb1a5ccd564f19c848fe9349586bfb8ce52af8682d1dc37e2a3; WM_TID=opyJCGkLpOlEERQFRUJ4llLsaBAcT9cU; __utma=63145271.661424980.1550992805.1550992805.1550994952.2"

headers= {"User-Agent" : "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
         "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
         "Accept-Language" : "en-us",
         "Connection" : "keep-alive",
         "Accept-Charset" : "GB2312,utf-8;q=0.7,*;q=0.7",
         "cookie": cookie
}

data = {'courseId': '93001', 'pageIndex': '1', 'pageSize': '20', 'orderBy': '3'}

response = requests.post(url, data, headers=headers)

# page count: "totlePageCount":35

print(response.text)

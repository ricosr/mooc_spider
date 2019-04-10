#encoding:utf-8
from flask import Flask,jsonify,render_template,request,redirect,url_for,session
from flask_pymongo import PyMongo
import pymongo
import json
import os
from bson.objectid import ObjectId
from decorators import login_required
from datetime import datetime
from Cathy_build_search_get_query_resultdb_set import search_index
from flask_paginate import Pagination, get_page_parameter
from Cathy_set_info import set_info
from client import load_clients, select_client


DB_OPT = None

app=Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

app.config.update(
    MONGO_HOST='localhost',
    MONGO_PORT=27017,
    MONGO_URI='mongodb://localhost:27017/soke',
    MONGO_DBNAME="soke",
)

mongo = PyMongo(app)


con=None
l=None


def connect_db(db_str):
    client = pymongo.MongoClient("mongodb://super_sr:comppolyuhk@209.97.166.185:27017/admin")
    # Caution: When uploading or sharing, remember to hide the sensitive information.
    db_opt = client[db_str]
    return db_opt


def get_aim_course(lec_id):
    # lec_id = list(return_dict.values())
    global DB_OPT
    db_opt = DB_OPT
    middle_list = list()
    general = db_opt['general']
    document = general.find()
    for x in document:
        # print(x)
        # print(str(x['lec_id']))
        if x['lec_id'] in lec_id:
            middle_list.append(x)
    return middle_list


@app.route('/',methods=['GET','POST'])
def index():

    if request.method == 'GET':
        return render_template('index.html')
    else:
        query = request.form.get('query')               #从表单中获取用户的输入
        cli, index = select_client()
        response_json = cli.get_response(query, index)
        response_dict = json.loads(response_json)

        global con
        global l
        print(query)
        seta = search_index(query)

        # con =  set_info(seta)
        # print(con)

        # con = [{ "_id" : ObjectId("5cad6bf62983981724f41392"),
        #          "lec_id" : 1003557005,
        #          "average" : 4.875,
        #          "count" : 8,
        #          "lec_name" : "软件项目管理",
        #          "school_name" : "北京邮电大学",
        #          "vip" : 0,
        #          "emotion":1,
        #          "img_url" : "http://edu-image.nosdn.127.net/1D86CCF8C169C5F824A3876E7FE5EAA3.jpg?imageView&thumbnail=510y288&quality=100",
        #          "lec_url" : "https://www.icourse163.org/course/BUPT-1003557005",
        #          "teachers" : [ "韩万江", "张笑燕", "陆天波", "杨金翠", "孙艺" ] },
        #        {"_id": ObjectId("5cad6bf62983981724f41394"),
        #         "lec_id": 1003557004,
        #         "average": 4.2,
        #         "count": 9,
        #         "lec_name": "python",
        #         "school_name": "深圳大学",
        #         "vip": 1,
        #         "emotion": 0.5,
        #         "img_url": "http://edu-image.nosdn.127.net/1D86CCF8C169C5F824A3876E7FE5EAA3.jpg?imageView&thumbnail=510y288&quality=100",
        #         "lec_url": "https://www.icourse163.org/course/BUPT-1003557005",
        #         "teachers": ["韩万江", "张笑燕", "陆天波", "杨金翠", "孙艺"]},
        #         {"_id": ObjectId("5cad6bf62983981724f41395"),
        #          "lec_id": 1003557003,
        #          "average": 4.5,
        #          "count":  100,
        #          "lec_name": "python",
        #          "school_name": "香港理工大学",
        #          "vip": 0,
        #          "emotion": -0.5,
        #          "img_url": "http://edu-image.nosdn.127.net/1D86CCF8C169C5F824A3876E7FE5EAA3.jpg?imageView&thumbnail=510y288&quality=100",
        #          "lec_url": "https://www.icourse163.org/course/BUPT-1003557005",
        #          "teachers": ["韩万江", "张笑燕", "陆天波", "杨金翠", "孙艺"]}
        #
        #        ]

        # templ={'T1554893778_1054852': [93001, 1001752002, 268001]}
        # l=list(templ.keys())[0]
        # print(type(l))

        # print(l)
        l = list(response_dict.keys())[0]
        con = get_aim_course(list(response_dict.values())[0])


        return render_template('search.html', con=con,l=l)
        # else:
        #     return '无相关搜索结果'

@app.route('/test')
def test():

    return render_template('test.html')




@app.route('/result')
def result():
    question = mongo.db.questions
    context = {
        'questions': question.find().sort("create_time", -1)
    }
    return render_template('result.html', **context)


@app.route('/login/',methods=['GET','POST'])
def login():
    user = mongo.db.users
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        print(telephone)
        password = request.form.get('password')
        result = user.find_one({'telephone': telephone,'password':password})
        #print(result)
        if result:
            #print(result['_id'])
            session['user_id'] = str(result['_id'])
            #如果想在31天内都不需要登陆
            #print(session['user_id'])
            session.permanent=True
            return redirect(url_for('index'))
        else:
            return '手机号码或者密码错误'

@app.route('/regist/',methods=['GET','POST'])
def regist():
    user = mongo.db.users
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #手机号码验证
        if user.find_one({'telephone': telephone}):
            # u=user.find_one({'telephone': telephone})
            # print(u['telephone'])
            return "重复"
        else:
            #password1和password2要相同
            if password1==password2:
                user.update(
                    {'telephone': telephone},
                    {
                        '$set': {'username': username, 'password': password1}
                    },
                    upsert=True
                )
                mongo.db.session.insert({'user_id':session['user_id'],'telephone': telephone,'username': username, 'password': password1})
                mongo.db.session.commit()
            #如果注册成功，跳转
            return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    #session.pop('user_id')
    #del session('user_id')
    session.clear()
    return redirect(url_for('login'))

@app.route('/question/', methods=['GET','POST'])
@login_required
def question():
    question = mongo.db.questions
    user = mongo.db.users
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = session.get('user_id')
        result = user.find_one({'_id':ObjectId(user_id)})
        #print(result)
        author = result['username']
        create_time = datetime.now()
        question.insert({'title': title,'content': content,'author':author,'create_time':create_time})
        # mongo.db.session.insert({'user_id':session['user_id'],'title': title, 'content': content,'author':author})
        # mongo.db.session.commit()
        return redirect(url_for('index'))


@app.route('/searchall/',methods=['get', 'post'])
def searchall():
    # con=[{'_id': ObjectId('5c9e29b62983981fdc1cebc7'), 'lec_id': 93001, 'average': 4.887005649717514, 'lec_name': '数据结构', 'school_name': '浙江大学', 'img_url': 'http://edu-image.nosdn.127.net/C4C10C0C27254ED77925331F19F83FED.jpg?imageView&thumbnail=510y288&quality=100', 'flag': 1}, {'_id': ObjectId('5c9e29ba2983981fdc1cebc8'), 'lec_id': 268001, 'average': 4.853004548719176, 'lec_name': 'Python语言程序设计', 'school_name': '北京理工大学', 'img_url': 'http://edu-image.nosdn.127.net/5B8826377EE623C7B6328E8F8B8D2871.png?imageView&thumbnail=510y288&quality=100', 'flag': 1}, {'_id': ObjectId('5c9e29ba2983981fdc1cebca'), 'lec_id': 1001752002, 'average': 4.656603773584906, 'lec_name': '多媒体技术及应用', 'school_name': '深圳大学', 'img_url': 'http://edu-image.nosdn.127.net/DE9AC030A30A85E0CBF85A84280EF747.jpg?imageView&thumbnail=426y240&quality=100', 'flag': 1}]
    global con
    return render_template('searchall.html',con=con)

@app.route('/searchscore/',methods=['get', 'post'])
def searchscore():
    # con=[{'_id': ObjectId('5c9e29b62983981fdc1cebc7'), 'lec_id': 93001, 'average': 4.887005649717514, 'lec_name': '数据结构', 'school_name': '浙江大学', 'img_url': 'http://edu-image.nosdn.127.net/C4C10C0C27254ED77925331F19F83FED.jpg?imageView&thumbnail=510y288&quality=100', 'flag': 1}, {'_id': ObjectId('5c9e29ba2983981fdc1cebc8'), 'lec_id': 268001, 'average': 4.853004548719176, 'lec_name': 'Python语言程序设计', 'school_name': '北京理工大学', 'img_url': 'http://edu-image.nosdn.127.net/5B8826377EE623C7B6328E8F8B8D2871.png?imageView&thumbnail=510y288&quality=100', 'flag': 1}, {'_id': ObjectId('5c9e29ba2983981fdc1cebca'), 'lec_id': 1001752002, 'average': 4.656603773584906, 'lec_name': '多媒体技术及应用', 'school_name': '深圳大学', 'img_url': 'http://edu-image.nosdn.127.net/DE9AC030A30A85E0CBF85A84280EF747.jpg?imageView&thumbnail=426y240&quality=100', 'flag': 1}]
    global con
    return render_template('searchscore.html',con=con)


@app.route('/searchsense/',methods=['get', 'post'])
def searchsense():
    # con=[{'_id': ObjectId('5c9e29b62983981fdc1cebc7'), 'lec_id': 93001, 'average': 4.887005649717514, 'lec_name': '数据结构', 'school_name': '浙江大学', 'img_url': 'http://edu-image.nosdn.127.net/C4C10C0C27254ED77925331F19F83FED.jpg?imageView&thumbnail=510y288&quality=100', 'flag': 1}, {'_id': ObjectId('5c9e29ba2983981fdc1cebc8'), 'lec_id': 268001, 'average': 4.853004548719176, 'lec_name': 'Python语言程序设计', 'school_name': '北京理工大学', 'img_url': 'http://edu-image.nosdn.127.net/5B8826377EE623C7B6328E8F8B8D2871.png?imageView&thumbnail=510y288&quality=100', 'flag': 1}, {'_id': ObjectId('5c9e29ba2983981fdc1cebca'), 'lec_id': 1001752002, 'average': 4.656603773584906, 'lec_name': '多媒体技术及应用', 'school_name': '深圳大学', 'img_url': 'http://edu-image.nosdn.127.net/DE9AC030A30A85E0CBF85A84280EF747.jpg?imageView&thumbnail=426y240&quality=100', 'flag': 1}]
    global con
    return render_template('searchsense.html',con=con)

@app.route('/searchcomment/',methods=['get', 'post'])
def searchcomment():
    # con=[{'_id': ObjectId('5c9e29b62983981fdc1cebc7'), 'lec_id': 93001, 'average': 4.887005649717514, 'lec_name': '数据结构', 'school_name': '浙江大学', 'img_url': 'http://edu-image.nosdn.127.net/C4C10C0C27254ED77925331F19F83FED.jpg?imageView&thumbnail=510y288&quality=100', 'flag': 1}, {'_id': ObjectId('5c9e29ba2983981fdc1cebc8'), 'lec_id': 268001, 'average': 4.853004548719176, 'lec_name': 'Python语言程序设计', 'school_name': '北京理工大学', 'img_url': 'http://edu-image.nosdn.127.net/5B8826377EE623C7B6328E8F8B8D2871.png?imageView&thumbnail=510y288&quality=100', 'flag': 1}, {'_id': ObjectId('5c9e29ba2983981fdc1cebca'), 'lec_id': 1001752002, 'average': 4.656603773584906, 'lec_name': '多媒体技术及应用', 'school_name': '深圳大学', 'img_url': 'http://edu-image.nosdn.127.net/DE9AC030A30A85E0CBF85A84280EF747.jpg?imageView&thumbnail=426y240&quality=100', 'flag': 1}]
    global con
    return render_template('searchcomment.html',con=con)

@app.route('/searchvipyes/',methods=['get', 'post'])
def searchvipyes():
    # con=[{'_id': ObjectId('5c9e29b62983981fdc1cebc7'), 'lec_id': 93001, 'average': 4.887005649717514, 'lec_name': '数据结构', 'school_name': '浙江大学', 'img_url': 'http://edu-image.nosdn.127.net/C4C10C0C27254ED77925331F19F83FED.jpg?imageView&thumbnail=510y288&quality=100', 'flag': 1}, {'_id': ObjectId('5c9e29ba2983981fdc1cebc8'), 'lec_id': 268001, 'average': 4.853004548719176, 'lec_name': 'Python语言程序设计', 'school_name': '北京理工大学', 'img_url': 'http://edu-image.nosdn.127.net/5B8826377EE623C7B6328E8F8B8D2871.png?imageView&thumbnail=510y288&quality=100', 'flag': 1}, {'_id': ObjectId('5c9e29ba2983981fdc1cebca'), 'lec_id': 1001752002, 'average': 4.656603773584906, 'lec_name': '多媒体技术及应用', 'school_name': '深圳大学', 'img_url': 'http://edu-image.nosdn.127.net/DE9AC030A30A85E0CBF85A84280EF747.jpg?imageView&thumbnail=426y240&quality=100', 'flag': 1}]
    global con
    print(con)
    conyes=[]
    for i in con:
        if i["vip"]==1:
            print(i)
            conyes.append(i)
        else:
            continue
    print(conyes)
    return render_template('searchvipyes.html',conyes=conyes)

@app.route('/searchvipno/',methods=['get', 'post'])
def searchvipno():
    # con=[{'_id': ObjectId('5c9e29b62983981fdc1cebc7'), 'lec_id': 93001, 'average': 4.887005649717514, 'lec_name': '数据结构', 'school_name': '浙江大学', 'img_url': 'http://edu-image.nosdn.127.net/C4C10C0C27254ED77925331F19F83FED.jpg?imageView&thumbnail=510y288&quality=100', 'flag': 1}, {'_id': ObjectId('5c9e29ba2983981fdc1cebc8'), 'lec_id': 268001, 'average': 4.853004548719176, 'lec_name': 'Python语言程序设计', 'school_name': '北京理工大学', 'img_url': 'http://edu-image.nosdn.127.net/5B8826377EE623C7B6328E8F8B8D2871.png?imageView&thumbnail=510y288&quality=100', 'flag': 1}, {'_id': ObjectId('5c9e29ba2983981fdc1cebca'), 'lec_id': 1001752002, 'average': 4.656603773584906, 'lec_name': '多媒体技术及应用', 'school_name': '深圳大学', 'img_url': 'http://edu-image.nosdn.127.net/DE9AC030A30A85E0CBF85A84280EF747.jpg?imageView&thumbnail=426y240&quality=100', 'flag': 1}]
    global con
    print(con)
    conno = []
    for i in con:
        if i["vip"] == 0:
            print(i)
            conno.append(i)
        else:
            continue
    print(conno)
    return render_template('searchvipno.html', conno=conno)



@app.route('/comment/<lec_id>',methods=['get', 'post'])
def comment(lec_id):
    print(lec_id)
    # lec={'lec_id':1,
    #      'agreeCount':50,#赞同数
    #      'mark':5.5,#星级
    #      'content':'很不错啊',
    #      'reply':"那里不错"
    #      }
    # lecture = mongo.db.lectures
    lec_id=268001
    print(lec_id)
    global l
    print(l)
    client = pymongo.MongoClient("mongodb://super_sr:comppolyuhk@209.97.166.185:27017/admin")
    db = client["temporary_comment"]
    lecture = db[l]
    # g=lecture.find({'lec_id': lec_id})
    g = lecture.find()
    for k in g:
        print(k)
    context = {
        'lectures': lecture.find({'lec_id': lec_id}).sort("agreeCount", -1),
        'size':lecture.find({'lec_id': lec_id}).count()
    }

    return render_template('comment.html',**context)

@app.route('/aboutus/')
def aboutus():

    return render_template('aboutus.html')





@app.context_processor
def my_context_processor():
    user = mongo.db.users
    user_id=session.get('user_id')
    #print(user_id)
    if user_id:
        result = user.find_one({'_id':ObjectId(user_id)})
        #print(result)
        if result:
            return {'result':result}
    return {}


if __name__ == '__main__':
    load_clients()
    DB_OPT = connect_db("course_info")
    app.run(debug=  True)
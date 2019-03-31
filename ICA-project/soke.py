#encoding:utf-8
from flask import Flask,jsonify,render_template,request,redirect,url_for,session
from flask_pymongo import PyMongo
import json
import os
from bson.objectid import ObjectId
from decorators import login_required
from datetime import datetime
from Cathy_build_search_get_query_resultdb_set import search_index
from flask_paginate import Pagination, get_page_parameter
from Cathy_set_info import set_info



app=Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

app.config.update(
    MONGO_HOST='localhost',
    MONGO_PORT=27017,
    MONGO_URI='mongodb://localhost:27017/soke',
    MONGO_DBNAME="soke",
)

mongo = PyMongo(app)




@app.route('/',methods=['GET','POST'])
def index():

    if request.method == 'GET':
        return render_template('index.html')
    else:
        query = request.form.get('query') #从表单中获取用户的输入
        print(query)

        seta = search_index(query)
        con =  set_info(seta)
        print(con)
        #
        # con = [{'lec_id': 1, 'average': 4.652, 'lec_name': '多媒体技术及应用', 'school_name': '深圳大学',
        #         'img_url': 'http://edu-image.nosdn.127.net/DE9AC030A30A85E0CBF85A84280EF747.jpg?imageView&thumbnail=426y240&quality=100',
        #         'flag': 1},
        #        {'lec_id': 2, 'average': 4.653, 'lec_name': '多媒体技术及应用',
        #         'school_name': '湖南大学',
        #         'img_url': 'http://edu-image.nosdn.127.net/DE9AC030A30A85E0CBF85A84280EF747.jpg?imageView&thumbnail=426y240&quality=100',
        #         'flag': 1}]

        return render_template('search.html', **locals())
        # else:
        #     return '无相关搜索结果'




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

    app.run(debug=  True)
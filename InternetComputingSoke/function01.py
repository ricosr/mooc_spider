# 增删查改
import pymongo
import time
import os
import shutil
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh.index import create_in, open_dir
from whoosh import sorting
from whoosh.qparser import MultifieldParser,QueryParser
from jieba.analyse import ChineseAnalyzer
analyzer = ChineseAnalyzer()


# This method is used to connect to a Database.
# db_str is the name of the Database.
def connect_db(db_str):
    client = pymongo.MongoClient("mongodb://super_sr:comppolyuhk@209.97.166.185:27017/admin")
    # Caution: When uploading or sharing, remember to hide the sensitive information.
    db_opt = client[db_str]
    return db_opt


# This method is used to read the content of each collection in the designated database.
# db_str is the name of the Database
# It calls method: connect_db
def read_db(db_str):
    db_opt = connect_db(db_str)
    collections_names = db_opt.list_collection_names()
    collections_names.remove('system.indexes')
    # for collection in collections_names[:5]: this aims to test 5 collections in order to save time
    start = time.perf_counter()
    for collection in collections_names[:5]:  # TODO
        print(next(db_opt[collection].find()))  # 1.4308634230000001
        # for x in db_opt[collection].find(): # 2.83240298
        #     print(x)
        #     print("1") # use to separate
        # **************************************************
        # print(db_opt[collection].find())
        # <pymongo.cursor.Cursor object at 0x03642810>
        # ***************************************************
        # dicta = next(db_opt[collection].find())
        # build_index(dicta)
        # 一开始我是想读一条就建一下索引，但是这样功能划分感觉很不清楚，read db中嵌套了build index
        # 那么假如先读取数据再来建索引的话，得到的返回值有会占用大量的内存
        # 因此，还是读一条建一个索引的方式，只不过这样拆分函数，read db改成get col name，建索引中再来连一次数据库？还是不对，算了直接建索引吧
        # 这个函数用来测试一下遍历数据库数据方法的速度吧。next() function is faster. 其实最好本地来测速；不然有网络速度干扰。
    end = time.perf_counter()
    print(end - start)


def refresh_index_file(index_dir):
    schema = Schema(  # 书写规范：schema等号两侧不要有空格
        content=TEXT(stored=True, analyzer=analyzer),  # 评论内容
        mark=NUMERIC(stored=True, sortable=True),  # 评价分数
        agreeCount=NUMERIC(stored=True, sortable=True),  # MOOC评价赞同数
        reply=TEXT(stored=True),  # 网易云针对评价的回复
        lec_id=NUMERIC(unique=True, sortable=True, stored=True)  # 课程编号
    )
    # each time we build an index, we should remove the old index, in case the crawled data has changed.
    # we design a two day fresh time.
    # ************* delete the old index , then build a new one ***************
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    else:
        # dellist = []
        deldir = index_dir
        dellist = os.listdir(deldir)
        for f in dellist:
            filePath = os.path.join(deldir, f)
            if os.path.isfile(filePath):
                os.remove(filePath)
                print(filePath + " was removed!")
            elif os.path.isdir(filePath):
                shutil.rmtree(filePath, True)
            print("Old index directory: " + filePath + " was removed!")
    create_in(index_dir, schema)


# def open_index(index_dir):
#     ix = open_dir(index_dir)
#     return ix


def build_index(db_str, index_dir):
    # **************** start to build index, each time read a collection, add an index document ************
    ix = open_dir(index_dir)
    writer = ix.writer()
    db_opt = connect_db(db_str)
    # 本来这边想改成传输数据库对象的，但是发现下面要根据名字进行判断，要得到它的名字很麻烦。
    collections_names = db_opt.list_collection_names()
    collections_names.remove('system.indexes')
    for collection in collections_names[:5]:  # TODO
        print(next(db_opt[collection].find()))
        col = next(db_opt[collection].find())
        comment = col["comments"]  # collection:col is a dict, comment is a list
        # for inner in range(len(comment)):#TypeError: 'int' object is not subscriptable
        if db_str == "mooc_db_sr":
            for inner in comment:  # inner is a dict
                writer.add_document(
                    lec_id=col['lec_id'],  # ValueError: 93001 is not unicode or sequence
                    content=inner['content'],  # TypeError: 'int' object is not subscriptable
                    # mark=comment[inner]['mark'],
                    mark=inner['mark'],
                    agreeCount=inner['agreeCount'],
                    reply=''
                )
                # 这边的reply本来想直接没有为null，但是为了方便还是设一个值吧。
        elif db_str == "net_db_sr":
            for inner in comment:  # inner is a dict
                writer.add_document(
                    lec_id=col['lec_id'],  # ValueError: 93001 is not unicode or sequence
                    content=inner['content'],  # TypeError: 'int' object is not subscriptable
                    # mark=comment[inner]['mark'],
                    mark=inner['mark'],
                    reply=inner['reply'],
                    agreeCount=0
                )
                # 这边的agreecount本来想直接没有为null，但是为了方便还是设一个值吧。
        # 上方的for in循环功能是替换的了本来的add_document(),取代了手工进行2索引，直接从数据库中读取数据建立索引。
    writer.commit()


# 搜索
def search_index(query, index_dir, db_opt):
    lec_ids = sorting.FieldFacet("lec_id")
    agreeCounts = sorting.FieldFacet("agreeCount", reverse=True)
    marks = sorting.FieldFacet("mark", reverse=True)
    ix = open_dir(index_dir)
    with ix.searcher() as searcher:
        parser = QueryParser("content", ix.schema)
        myquery = parser.parse(query)
        # 一开始这里失败了，是由于txt文件的编码形式不是UTF-8，导致了乱码。
        # results = searcher.search(myquery,limit=None)
        # results = searcher.search_page(myquery, 5) # 得到第五页的内容，还是第六页？，每页多少个来着
        results = searcher.search(myquery, limit=None, sortedby=[lec_ids, agreeCounts,marks])
        print(len(results))  # 评论命中个数
        # print(type(results)) # <class 'whoosh.searching.Results'>
        # print(results[:])
        # for i in range(len(results)):
        #     print(results[i]);print('\n') #IndexError: results[10]: Results only has 10 hits
        # *************************************************
        # print(results)

        # *************************************************
        # return comment_into_db(results, de_db)


# def comment_into_db(results, db_str):
        count = 0
        # db_opt = connect_db(db_str)
        b = list()
        return_dict = dict()
        # 把所有命中的评论放入course_info数据库的aim_comment集合中，每次查询需要清空原有数据
        # x = db_opt.aim_comment.delete_many({})
        #
        # print(x.deleted_count, "个文档已删除")
        for i in results:
            # count += 1
            # print(i)  # 打印出每一个命中的评论
            # <Hit {'content': '为什么用记事本', 'lec_id': 1004943019, 'mark': 5.0, 'reply': '这个可能是Hbuilder工具出了些小问题'}>
            j = dict(i)
            print(j)
            aim_comment = str(time.time())  # TODO
            db_opt[aim_comment].insert_one(
                {'lec_id': j['lec_id'],
                 'agreeCount': j['agreeCount'],
                 'mark': j['mark'],
                 'content': j['content'],
                 'reply': j['reply']}
            )
            b.append(j['lec_id'])
        lec_list = list(set(b))
        return_dict[aim_comment] = lec_list
        # print(count)
        print(return_dict)
        return return_dict
        # context = set_info(seta)
        # return context


def cal_lec_info(db_opt, de_db):
    # db_opt = connect_db()
    collections_names = db_opt.list_collection_names()
    collections_names.remove('system.indexes')
    # course = pymongo.MongoClient("mongodb://super_sr:123456@209.97.166.185:27017/admin")
    # db_course = course["course_info"]
    general = de_db.general
    lec_general = dict()
    for collection in collections_names[:5]:  # TODO
        sum_grade = 0
        count = 0
        print(next(db_opt[collection].find()))
        collection = next(db_opt[collection].find())
        comment = collection["comments"]  # collection is a dict, comment is a list
        lec_id = collection['lec_id']
        lec_name = collection['lec_name']
        school_name = collection['school_name']
        img_url = collection['img_url']
        # lec_name = collection['lec_name']
        for inner in comment:  # inner is a dict
                mark = inner['mark']
                sum_grade += mark
                count += 1
        average = sum_grade/count
        # general.insert_one(
        # {'lec_id': lec_id, 'average': average, 'lec_name':lec_name, 'school_name':school_name,
        # 'img_url':img_url, 'flag':0})
        # flag是用来标注命中的课程的。0为初始值，1为命中的课程
        general.insert_one(
            {'lec_id': lec_id, 'average': average, 'lec_name': lec_name, 'school_name': school_name, 'img_url': img_url,
             'flag': 0})

        lec_grade[lec_id] = average
    return lec_grade


def set_info(seta):
    course = pymongo.MongoClient("mongodb://super_sr:comppolyuhk@209.97.166.185:27017/admin")
    db_course = course["course_info"]
    grade = db_course.grade
    lista = list(seta)
    for i in range(len(lista)):
        myquery = {"lec_id": lista[i]}
        newvalues = {"$set": {"flag":1}}
        grade.update_one(myquery, newvalues)
    b = grade.find({"flag":1}).sort("average",-1)






    c = list()
    for x in b:
        # print(type(x))
        c.append(x)
    # b = grade.find({"flag: 1"}).sort("average", -1)
    # TypeError: filter must be an instance of dict, bson.son.SON, or other type that inherits from collections.Mapping
    # context = {
    #     'contexts':b
    # }
    return c

def write_db(dict_obj, db_opt):
    posts = db_opt['M' + str(dict_obj["lec_id"])]
    posts.insert(dict_obj)
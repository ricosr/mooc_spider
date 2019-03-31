# This Python file is intended to get 5 collections from MongoDB,and build an index according to the schema.
# Then I can test if I can search any query within the index.
from parse_mooc_comments_json import read_comments_info, COMMENTS_DATA
from whoosh.fields import Schema, TEXT, ID, NUMERIC
import os
from whoosh.index import create_in, open_dir
from jieba.analyse import ChineseAnalyzer
analyzer = ChineseAnalyzer()
import pymongo
def connect_db():
    client = pymongo.MongoClient("mongodb://address")
    db_opt = client["mooc_db_sr"]
    return db_opt

def read_db():
    db_opt = connect_db()
    collections_names = db_opt.list_collection_names()
    #DeprecationWarning: collection_names is deprecated. Use list_collection_names instead
    collections_names.remove('system.indexes')
    #f = open("C:\\Users\\Catherine\\PycharmProjects\\InternetComputingGP\\temp-mooc.txt",'w')
    for collection in collections_names[:5]:
        #f.write(next(db_opt[collection].find()))
        print(next(db_opt[collection].find()))
        dicta = next(db_opt[collection].find())
        build_index(dicta)
    #f.close()

def build_index(collection):
    schema = Schema(
        content=TEXT(stored=True, analyzer=analyzer),#评论内容
        mark=NUMERIC(stored=True),# 评价分数
        agreeCount=NUMERIC(stored=True), #评价赞同数
        lec_id=NUMERIC(unique=True, stored=True) #课程编号
    )
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
        # create_in("C:\\Users\\Catherine\\PycharmProjects\\InternetComputingGP\\testindexdir", schema)
        create_in("indexdir", schema)
    ix = open_dir("indexdir")
    writer = ix.writer()
    # for bm in comment_collection.find(timeout=False): #TypeError: __init__() got an unexpected keyword argument 'timeout'
    # 貌似是由于版本Python2.x更新之后timeout参数没有了
    # for outer in collection:
    # #for outer in collection.find():
    #     comment = outer['comment']
    #     for inner in range(len(comment)):
    #         writer.add_document(
    #             lec_id=outer['lec_id'],
    #             content=comment[inner]['content'],
    #             mark=comment[inner]['mark'],
    #             agreeCount=comment[inner]['agreeCount'],
    #
    #         )
    comment = collection["comments"] #collection is a dict, comment is a list
    # for inner in range(len(comment)):#TypeError: 'int' object is not subscriptable
    for inner in comment: #inner is a dict
        writer.add_document(
            lec_id=collection['lec_id'], #ValueError: 93001 is not unicode or sequence
            content=inner['content'], #TypeError: 'int' object is not subscriptable
            #mark=comment[inner]['mark'],
            mark=inner['mark'],
            agreeCount=inner['agreeCount']
        # raise ValueError("%r is not unicode or sequence" % value)

            )
    # 上方的for in循环功能是替换的了本来的add_document(),取代了手工进行2索引，直接从数据库中读取数据建立索引。
    writer.commit()

read_db()
# 搜索
from whoosh.qparser import MultifieldParser,QueryParser
ix = open_dir("indexdir")
with ix.searcher() as searcher:
    #query = MultifieldParser(["url", "title", "tags", "note", "article"], ix.schema).parse("使用")
    parser = QueryParser("content", ix.schema)
    myquery = parser.parse("使用")
    #一开始这里失败了，是由于txt文件的编码形式不是UTF-8，导致了乱码。
    results = searcher.search(myquery)
    print(len(results))
    print(type(results))
    #print(results[:])
    # for i in range(len(results)):
    #     print(results[i]);print('\n') #IndexError: results[10]: Results only has 10 hits
    print(results)
    count = 0
    for i in results:
        count += 1
        print(i);print('\n')
    print(count)



import pymongo
def connect_db():
    client = pymongo.MongoClient("mongodb://address")
    db_opt = client["mooc_db_sr"]
    return db_opt

def cal_lec_grade():
    db_opt = connect_db()
    collections_names = db_opt.list_collection_names()
    collections_names.remove('system.indexes')
    lec_grade = dict()
    for collection in collections_names[:5]:
        sum = 0
        count = 0
        print(next(db_opt[collection].find()))
        collection = next(db_opt[collection].find())
        comment = collection["comments"]  # collection is a dict, comment is a list
        lec_id = collection['lec_id']
        # lec_name = collection['lec_name']
        for inner in comment:  # inner is a dict
                mark=inner['mark']
                sum += mark
                count += 1
        average = sum/count
        lec_grade[lec_id] = average
    return lec_grade

lec_grade = cal_lec_grade()
print(lec_grade)

items = list(lec_grade.items())
items.sort(key=lambda x:x[1],reverse=True)
client = pymongo.MongoClient("mongodb://address")
db_opt = client["course_info"]
grade = db_opt.grade
#grade.drop()
for i in range(len(items)):
    word,count = items[i]
    grade.insert_one({'lec_id':word,'mark':count}) #DeprecationWarning: insert is deprecated. Use insert_one or insert_many instead.
    #grade.insert({'lec_id':word,'mark':count})
    print("{:<15}{:>15}".format(word,count))




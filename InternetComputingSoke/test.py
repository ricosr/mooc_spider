from function01 import *

# read_db("mooc_db_sr")

# *************************

index_dir = "indexdir"
refresh_index_file(index_dir)
build_index("mooc_db_sr", index_dir)
build_index("net_db_sr", index_dir)

# de_db = connect_db('course_info')
# result = search_index('记事本', index_dir, de_db)
# set_info(result)




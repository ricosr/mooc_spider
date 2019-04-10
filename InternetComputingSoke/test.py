from function01 import *

# read_db("mooc_db_sr")

# *************************

#index_dir = "indexdir"
# refresh_index_file(index_dir)
# build_index("mooc_db_sr", index_dir)
# build_index("net_db_sr", index_dir)

# de_db = connect_db('temporary_comment')
# result = search_index('使用', index_dir, de_db)
# lec_id = list(result.values())[0]  # [[93001, 1001752002, 268001]]
# # print(lec_id)
# get_aim_course(lec_id)

del_col('course_info', 'general')
de_db = connect_db('course_info')
cal_lec_info('mooc_db_sr', de_db)
cal_lec_info('net_db_sr', de_db)






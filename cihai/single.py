#-*-coding:utf-8-*-
import json
import re
import mysql.connector
import sys
import time
import xlrd

config = {
    'user': 'root',
    'password': '******',
    'host': '127.0.0.1',
    'database': 'rhymes',
    'charset': 'utf8',
    "connection_timeout": 20,
    "use_pure": True,
    "auth_plugin": 'mysql_native_password',
}


# 打开文件
data = xlrd.open_workbook("汉字.xls")

# 查看工作表

#print("sheets：" + str(data.sheet_names()))

# 通过文件名获得工作表,获取工作表1
table = data.sheet_by_name('Sheet1')
# print("总行数：" + str(table.nrows))
# print("总列数：" + str(table.ncols))
#
# print("整行值：" + str(table.row_values(0,0)))
# print("整列值：" + str(table.col_values(0,0)))

mydb = mysql.connector.connect(**config)
mycs = mydb.cursor(dictionary=True)

for rowNum in range(table.nrows):

    if rowNum > 0:
        rr = table.row_values(rowNum)[0]
        yin = table.row_values(rowNum)[1]

        key1 = re.findall('iang|ian|iao|ia|iong|uai|uang|uan|ua|uo|ang|eng|ing|ong|ai|ei|ui|ao|ou|iu|ie|ue|er|an|en|in|un|a|o|e|i|u', yin)
        for c in rr:
            insertlist = list()
            insertlist.append("".join(c))
            insertlist.append("".join(yin))
            insertlist.append("".join(key1))
            print(insertlist)
            sql = "replace into cihai (words,yin,key1) values (%s,%s,%s)"
            mycs.execute(sql, insertlist)

    if not rowNum % 300:
        mydb.commit()

mydb.commit()
time.sleep(8)
mycs.close()
mydb.close()

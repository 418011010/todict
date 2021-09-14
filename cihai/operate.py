#-*-coding:utf-8-*-
import json
import re
import mysql.connector
import sys
import time

config = {
    'user': 'root',
    'password': 'coship',
    'host': 'localhost',
    'database': 'rhymes',
    'charset': 'utf8',
    "connection_timeout": 20,
    "use_pure": True,
    "auth_plugin": 'mysql_native_password',
}




def ins(mycs,yunlist,n,id):


    # print(mydb)
    if n == 5:
        sql = "update cihai  set yun=(%s),key1=(%s),key2=(%s),key3=(%s),key4=(%s),key5=(%s) where id={}".format(id)
        #mycs = mydb.cursor(dictionary=True)


        mycs.execute(sql, yunlist)
        #mydb.commit()  # 数据表内容有更新，必须使用到该语句
        print('已更新' + str(mycs.rowcount) + '条数据')



    elif n == 4:
        sql = "update cihai  set yun=(%s),key1=(%s),key2=(%s),key3=(%s),key4=(%s) where id={}".format(id)
        #mycs = mydb.cursor(dictionary=True)


        mycs.execute(sql, yunlist)
        #mydb.commit()  # 数据表内容有更新，必须使用到该语句
        print('已更新' + str(mycs.rowcount) + '条数据')

    elif n == 3:
        sql = "update cihai  set yun=(%s),key1=(%s),key2=(%s),key3=(%s) where id={}".format(id)
        #mycs = mydb.cursor(dictionary=True)


        mycs.execute(sql, yunlist)
        #mydb.commit()  # 数据表内容有更新，必须使用到该语句
        print('已更新' + str(mycs.rowcount) + '条数据')

    elif n == 2:
        sql = "update cihai  set yun=(%s),key1=(%s),key2=(%s) where id={}".format(id)
        #mycs = mydb.cursor(dictionary=True)


        mycs.execute(sql, yunlist)
        #mydb.commit()  # 数据表内容有更新，必须使用到该语句
        print('已更新' + str(mycs.rowcount) + '条数据')

    elif n == 1:
        sql = "update cihai  set yun=(%s),key1=(%s) where id={}".format(id)
        #mycs = mydb.cursor(dictionary=True)


        mycs.execute(sql, yunlist)

        print('已更新' + str(mycs.rowcount) + '条数据')

    else:
        print("参数不对")


def sqlproccess(n):
    try:
        mydb = mysql.connector.connect(**config)
    except Exception as e:

        print("数据库连接失败：" + str(e))
        log4 = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + '数据库连接失败\n' + str(e) + '\n'
        with open('inject.log', 'a', encoding='utf-8') as f:
            f.write(log4)
        sys.exit()

    sql1 = "SELECT yin FROM cihai where ID <{}".format(n)
    mycs = mydb.cursor(dictionary=True)



    mycs.execute(sql1)
    #mydb.commit()  # 数据表内容有更新，必须使用到该语句
    myresult = mycs.fetchall()
    #print(type(myresult))

    for index, x in enumerate(myresult):
        #print(x['yin'])

        x['yin'] = re.sub('ā|á|à|ǎ', 'a', x['yin'])
        x['yin'] = re.sub('ī|ì|í|ǐ', 'i', x['yin'])
        x['yin'] = re.sub('ō|ó|ǒ|ò', 'o', x['yin'])
        x['yin'] = re.sub('ū|ú|ǔ|ù', 'u', x['yin'])
        x['yin'] = re.sub('ē|é|ě|è', 'e', x['yin'])
        x['yin'] = re.sub('ǖ|ǘ|ǚ|ǜ', 'u', x['yin'])
        #print(x['yin'])5t4r
        sql2 = "UPDATE cihai SET yun='{}' WHERE ID={}".format(x['yin'], index+1)
        #mycs.execute(sql2)
        key = re.findall('iang|ian|iao|ia|iong|uai|uang|uan|ua|uo|ang|eng|ing|ong|ai|ei|ui|ao|ou|iu|ie|ue|er|an|en|in|un|a|o|e|i|u', x['yin'])
        #print(key)
        yunl = list()

        yunl.append(''.join(x['yin']))
        if len(key) >= 5:
            key5 = key[-5:]
            key4 = key[-4:]
            key3 = key[-3:]
            key2 = key[-2:]
            key1 = key[-1:]
            yunl.append(",".join(key1))
            yunl.append(",".join(key2))
            yunl.append(",".join(key3))
            yunl.append(",".join(key4))
            yunl.append(",".join(key5))
            #yunl.append(''.join(str(index + 1)))
            print(yunl)
            ins(mycs, yunl, 5, index+1)
        elif len(key) == 4:
            key4 = key[-4:]
            key3 = key[-3:]
            key2 = key[-2:]
            key1 = key[-1:]
            yunl.append(",".join(key1))
            yunl.append(",".join(key2))
            yunl.append(",".join(key3))
            yunl.append(",".join(key4))

            print(yunl)
            ins(mycs, yunl, 4, index+1)
        elif len(key) == 3:

            key3 = key[-3:]
            key2 = key[-2:]
            key1 = key[-1:]
            yunl.append(",".join(key1))
            yunl.append(",".join(key2))
            yunl.append(",".join(key3))

            print(yunl)
            ins(mycs, yunl, 3, index+1)
        elif len(key) == 2:

            key2 = key[-2:]
            key1 = key[-1:]
            yunl.append(",".join(key1))
            yunl.append(",".join(key2))

            print(yunl)
            ins(mycs, yunl, 2, index+1)
        elif len(key) == 1:

            key1 = key[-1:]
            yunl.append(",".join(key1))

            print(yunl)
            ins(mycs, yunl, 1, index+1)
        else:
            pass

        if not index % 5000:
            mydb.commit()

    mydb.commit()
    time.sleep(3)
    mycs.close()
    mydb.close()


sqlproccess(380580)

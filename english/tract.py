#-*-coding:utf-8-*-
import json
import re
import mysql.connector
import sys
import time


def mysq(orglist,n):
    config = {
        'user': 'root',
        'password': '******',
        'host': '127.0.0.1',
        'database': 'rhymes',
        'charset': 'utf8',
        "connection_timeout": 20,
        "use_pure": True
    }

    try:
        mydb = mysql.connector.connect(**config)
    except  Exception as e:

        print("数据库连接失败：" + str(e))
        log4 = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + '数据库连接失败\n' + str(e) + '\n'
        with open('inject.log', 'a', encoding='utf-8') as f:
            f.write(log4)
        sys.exit()

    # print(mydb)
    if n == 4:
        sql = "replace INTO words (word,pron,ch,key1,key2,key3,key4) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        mycs = mydb.cursor(dictionary=True)

        try:

            mycs.executemany(sql, orglist)
            mydb.commit()  # 数据表内容有更新，必须使用到该语句
            print('已更新' + str(mycs.rowcount) + '条数据')

        except Exception as e:
            mydb.rollback()
            print("导入失败：" + str(e))
            log5 = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + '导入失败\n' + str(e) + '\n'
            with open('inject.log', 'a', encoding='utf-8') as f:
                f.write(log5)
        finally:
            mycs.close()
            mydb.close()

    elif n == 3:
        sql = "replace INTO words (word,pron,ch,key1,key2,key3) VALUES (%s,%s,%s,%s,%s,%s)"
        mycs = mydb.cursor(dictionary=True)

        try:

            mycs.executemany(sql, orglist)
            mydb.commit()  # 数据表内容有更新，必须使用到该语句
            print('已更新' + str(mycs.rowcount) + '条数据')

        except Exception as e:
            mydb.rollback()
            print("导入失败：" + str(e))
            log5 = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + '导入失败\n' + str(e) + '\n'
            with open('inject.log', 'a', encoding='utf-8') as f:
                f.write(log5)
        finally:
            mycs.close()
            mydb.close()

    elif n == 2:
        sql = "replace INTO words (word,pron,ch,key1,key2) VALUES (%s,%s,%s,%s,%s)"
        mycs = mydb.cursor(dictionary=True)

        try:

            mycs.executemany(sql, orglist)
            mydb.commit()  # 数据表内容有更新，必须使用到该语句
            print('已更新' + str(mycs.rowcount) + '条数据')

        except Exception as e:
            mydb.rollback()
            print("导入失败：" + str(e))
            log5 = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + '导入失败\n' + str(e) + '\n'
            with open('inject.log', 'a', encoding='utf-8') as f:
                f.write(log5)
        finally:
            mycs.close()
            mydb.close()

    elif n == 1:
        sql = "replace INTO words (word,pron,ch,key1) VALUES (%s,%s,%s,%s)"
        mycs = mydb.cursor(dictionary=True)

        try:

            mycs.executemany(sql, orglist)
            mydb.commit()  # 数据表内容有更新，必须使用到该语句
            print('已更新' + str(mycs.rowcount) + '条数据')

        except Exception as e:
            mydb.rollback()
            print("导入失败：" + str(e))
            log5 = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + '导入失败\n' + str(e) + '\n'
            with open('inject.log', 'a', encoding='utf-8') as f:
                f.write(log5)
        finally:
            mycs.close()
            mydb.close()

    else:
        print("参数不对")




file_content = open('yh.txt', encoding='utf-8', errors='ignore')
clist = file_content.readlines()
words = {}
for i, val in enumerate(clist):
    #print(i, val)
    pattern = u'(.*?)	<.*?<pron>(.*?)</pron>.*?<span class="zh">(.*?)</span>'

    res = re.findall(pattern, val)

    if res:

        #print(res[0][1])
        key = re.findall('iː|ɜː|ɑː|ɔː|uː|eɪ|aɪ|ɔɪ|əʊ|aʊ|ɪə|eə|ʊə|ɪ|e|æ|ʌ|a|ʊ|ə|ɒ', res[0][1])
        if len(key) >= 4:
            key4 = key[-4:]
            key3 = key[-3:]
            key2 = key[-2:]
            key1 = key[-1:]
            res[0] = list(res[0])
            res[0].append(",".join(key1))
            res[0].append(",".join(key2))
            res[0].append(",".join(key3))
            res[0].append(",".join(key4))

            print(res)
            mysq(res, 4)
        elif len(key) == 3:
            key3 = key[-3:]
            key2 = key[-2:]
            key1 = key[-1:]
            res[0] = list(res[0])
            res[0].append(",".join(key1))
            res[0].append(",".join(key2))
            res[0].append(",".join(key3))

            print(res)
            mysq(res, 3)
        elif len(key) == 2:

            key2 = key[-2:]
            key1 = key[-1:]
            res[0] = list(res[0])
            res[0].append(",".join(key1))
            res[0].append(",".join(key2))

            print(res)
            mysq(res, 2)
        elif len(key) == 1:

            key1 = key[-1:]
            res[0] = list(res[0])
            res[0].append(",".join(key1))
            print(res)
            mysq(res, 1)
        else:
            pass


file_content.close()


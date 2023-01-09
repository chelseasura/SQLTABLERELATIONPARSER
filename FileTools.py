"""_summary_
   便利目录并找到SQL,然后以;拆成对应的
"""
import copy
import os
import re
import traceback

import chardet

from UtilsForSQLPARSER import parseSQLCreateTableAs

sqllineArr=[];  # 所有SQL语句放入数组中


# 获取文件编码类型
def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']


def walkpythonfiles(filepath=""):
    pass
    print("开始在指定目录下进行文件目录{path}解析...".format(path=filepath))
    walkpath = filepath
    regex_start = re.compile("^.*sql$")
    for file in os.listdir(walkpath):
        m = regex_start.findall(file)
        if m is not None and len(m) != 0:
            splitFileIntoSqlArray(sqlfile=m[0],thefilepath=filepath)
    for arr in sqllineArr:
        parseSQLLine(sqlline=arr)

'''
读取对应的SQL文件按照;结束符号把每一个语句塞入数据列表中
'''
def splitFileIntoSqlArray(thefilepath="",sqlfile=None):
    allwords=[]
    file=None
    print("读取脚本{file}".format(file=sqlfile))
    print(thefilepath)
    try:
        filepath = thefilepath+"/"+sqlfile
        filecoding = get_encoding(file=filepath)
        print("原始文件采用编码", filecoding)
        count = len(open(filepath, 'r', encoding=filecoding, errors="ignore").readlines())
        # 文本解析到具体的单词列表
        file = open(filepath, "r+", encoding=filecoding, errors="ignore")

        # 逐行逐个单词解读文本
        for index, line in enumerate(file.readlines()):
            if not re.match(r"^--|^#",line):
                pass
                for words in [x for x in re.split(r'(\t|\n|\s|\r)', line) if x]:
                    if re.search(r"[a-zA-Z0-9;,\?\*]", words, re.IGNORECASE)  :
                       pass
                       allwords.append(words)
        #print(allwords)
        linewords=[]
        for words in allwords:
            linewords.append(words)
            if ";" in words:
                pass
                #如上单词应该压入数据内容中
                sqllineArr.append(copy.deepcopy(linewords))
                linewords=[]
        #print(sqllineArr)
    except Exception as e:
        #把错误文件写到日志中
        msg = traceback.format_exc() # 方式1
        print (msg)
        pass
    finally:
        file.close()


'''
SQL 关键字参照
CREATE TABLE CREATE VIEW 
INSERT INTO MERGE INTO 
AS SELECT  FROM WHERE  
'''
def parseSQLLine(sqlline=[]):
    pass
    print("开始对语句{query}解析......".format(query=sqlline))
    if re.match(r"\s?create\s?table\s?.*as.*","".join(sqlline),re.IGNORECASE):
        pass
        print("探测到这个语句是一个利用建表语法处理数据的SQL")
        parseSQLCreateTableAs(sql=sqlline)
    else:
        print("当前SQL语句没有被匹配到......")




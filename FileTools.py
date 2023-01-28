"""_summary_
   便利目录并找到SQL,然后以;拆成对应的
"""
import copy
import os
import re
import traceback
import chardet
from UtilsForSQLPARSER import parseSQLCreateTableAs, parseSQLTruncate, parseSQLDropTable, parseSQLInsertInto
from Log import logger

sqllineArr=[];  # 所有SQL语句放入数组中


# 获取文件编码类型
def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']


def walkpythonfiles(filepath=""):
    pass
    logger.info("开始在指定目录下进行文件目录{path}下解析...".format(path=filepath))
    walkpath = filepath
    regex_start = re.compile("^.*sql$")
    for file in os.listdir(walkpath):
        m = regex_start.findall(file)
        if m is not None and len(m) != 0:
            logger.debug(str(m))
            splitFileIntoSqlArray(sqlfile=m[0],thefilepath=filepath)
    for theobject in sqllineArr:
        parseSQLLine(sqlline=theobject['sqlline'],sqlfile=theobject['sqlfile'])

'''
读取对应的SQL文件按照;结束符号把每一个语句塞入数据列表中
'''
def splitFileIntoSqlArray(thefilepath="",sqlfile=None):
    allwords=[]
    file=None
    logger.info("读取脚本{file}".format(file=sqlfile))
    logger.info(thefilepath)
    try:
        filepath = thefilepath+"/"+sqlfile
        filecoding = get_encoding(file=filepath)
        logger.info("原始文件采用编码{format}".format(format=filecoding))
        count = len(open(filepath, 'r', encoding=filecoding, errors="ignore").readlines())
        # 文本解析到具体的单词列表
        file = open(filepath, "r+", encoding=filecoding, errors="ignore")
        # 逐行逐个单词解读文本
        for index, line in enumerate(file.readlines()):
            if not re.match(r"^--|^#",line):
                for words in [x for x in re.split(r'(\t|\n|\s|\r)', line) if x != " " or x !=""]:
                    if re.search(r"[a-zA-Z0-9;,\?\*\(\)]", words, re.IGNORECASE):
                       allwords.append(words)
        logger.debug(allwords)
        linewords=[]
        for words in allwords:
            linewords.append(words)
            if ";" in words:
                pass
                #如上单词应该压入数据内容中
                dictobject={}
                dictobject['sqlline']=copy.deepcopy(linewords)
                dictobject['sqlfile']=filepath
                sqllineArr.append(dictobject)
                linewords=[]
        logger.debug("打印出所有的SQL语句数组")
        logger.debug(sqllineArr)
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
def parseSQLLine(sqlline=[],sqlfile=""):
    pass
    logger.info("开始对语句{query}解析......".format(query=sqlline))
    if re.match(r"\s?create\s?table\s?.*as.*","".join(sqlline),re.IGNORECASE):
        pass
        logger.info("探测到这个语句是一个利用建表语法处理数据的SQL")
        parseSQLCreateTableAs(sql=sqlline,sqlfile=sqlfile)
    elif re.match(r"\s?truncate\s?table\s?.*","".join(sqlline),re.IGNORECASE):
        pass
        logger.info("探测到这个语句是truncate语句")
        parseSQLTruncate(sql=sqlline,sqlfile=sqlfile)
    elif re.match(r"\s?drop\s?table\s?.*","".join(sqlline),re.IGNORECASE):
        logger.info("探测到这个语句是drop table 语句")
        parseSQLDropTable(sql=sqlline,sqlfile=sqlfile)
    elif re.match(r"\s?insert\s?into\s?.*","".join(sqlline),re.IGNORECASE):
        logger.info("探测到这个语句是insert into 语句")
        parseSQLInsertInto(sql=sqlline,sqlfile=sqlfile)
    else:
        logger.error("当前SQL语句没有被匹配到......")





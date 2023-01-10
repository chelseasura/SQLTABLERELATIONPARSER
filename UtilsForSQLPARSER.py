'''
create table as select * from b,c where

'''
import re
from Log import logger

global AllUsedTables;

#全量使用的数据表清单
AllUsedTables=[]

def parseSQLCreateTableAs(sql=[],sqlfile=""):
    global AllUsedTables
    pass
    #获取创建的表名
    result=re.sub(r"\s?create\s?table\s?",""," ".join(sql),0,re.IGNORECASE)
    result1=re.sub(r"\s?as.*","",result,0,re.IGNORECASE)
    result2=re.sub(r";","",result1,0,re.IGNORECASE)
    AllUsedTables.append(result2)
    logger.info("记录下获取的create 表名")
    logger.info(result2)
    fromtables=detachFromAfter(sql=sql)
    logger.info("探测当前SQL用到的表:")
    logger.info(fromtables)
    #排重操作
    AllUsedTables=list(set(AllUsedTables))
    logger.info(AllUsedTables)


def countNumOfItem(theitem,arr):
    count=0;
    for item in arr:
        if theitem==item:
            count+=1;
    return count

def detachFromTableNameFromSubQuery(sqlline):
    pass

#把from 后的查询块解析写在一个方法内
def detachFromAfter(sql=[]):
    tablesforuse=[]
    pass
    # 获取后面的数据
    result = re.sub(r"\s?create\s?table\s?.*from", "", " ".join(sql), 0, re.IGNORECASE)
    result1 = re.sub(r"\s?(where).*", "", result, 0, re.IGNORECASE)  # 如果多表关联形式的用where 和逗号表示
    logger.info("剩余内容截取{result}".format(result=result1))
    if "on" in sql:
        pass
        # 当前出现了join on 语法 探测一共出现了几个join 或者几个on
        countnum = countNumOfItem("join", sql)
        logger.info("一共出现{n}次JOIN连接".format(n=countnum))
        for joinline in result1.split("join"):
            logger.debug("按照join切割后的内容")
            logger.debug(joinline)
            result2 = re.sub(r"\s?(join|left\s?join|right\s?join|full\s?join|left|right|full)", "", joinline, 0,
                             re.IGNORECASE)  # 如果多表关联用的是join on 语法
            result3 = re.sub(r"on.*", "", result2, 1, re.IGNORECASE)
            AllUsedTables.append([x for x in re.split(r'(\t|\n|\s|\r)', result3) if x != ' ' and x != ''][0])
            tablesforuse.append([x for x in re.split(r'(\t|\n|\s|\r)', result3) if x != ' ' and x != ''][0])
    else:
        pass
        # 非join方式用表
        # 采用逗号
        logger.info("没有采用JOIN连接,把FROM后的表名摘入清单")
        # 判断是否是多表
        compilerx = re.compile(r"(\s|\n)?[^\s]+(\s)+[^\s]+,")
        if re.match(compilerx, result1):
            pass
            # 符合多,表名特点
            logger.info("多表名逗号关联操作")
            for splitsql in result1.split(","):
                # print(splitsql)
                logger.debug(splitsql)
                AllUsedTables.append([x for x in re.split(r'(\t|\n|\s|\r)', splitsql) if x != ' ' and x != ''][0])
                tablesforuse.append([x for x in re.split(r'(\t|\n|\s|\r)', splitsql) if x != ' ' and x != ''][0])
        else:
            pass
            logger.info("只用了一个表名")
            AllUsedTables.append([x for x in re.split(r'(\t|\n|\s|\r)', result1) if x != ' ' and x != ''][0])
            tablesforuse.append([x for x in re.split(r'(\t|\n|\s|\r)', result1) if x != ' ' and x != ''][0])
    return tablesforuse




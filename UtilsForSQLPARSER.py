'''
create table as select * from b,c where

'''
import re
from TableRelations import TableRelations
import colorlog
import logging

colorlog.basicConfig(level=logging.INFO)

global AllUsedTables, AllTableDict, AllFromTables;

# 脚本名和表关系
File_AllUsedTables = {}

# 所有产生依赖的清单
AllUsedTables = []

AllFromTables = []

# 表和表关系以及SQL脚本的工具
AllTableDict = {}

# 脚本和里面有的表的关系
scriptTables = {}


def parseSQLTruncate(sql=[], sqlfile=""):
    colorlog.info("要处理的语句是{sql}".format(sql="".join(sql)))
    result = re.sub(r"\s?truncate\s?table\s?", "", " ".join(sql), 0, re.IGNORECASE)
    result2 = re.sub(r";", "", result, 0, re.IGNORECASE)
    colorlog.info("最终获取到的表名")
    colorlog.info(result2)
    __packDataStruce(byname=result2, fromtables=None, sqlfile=sqlfile)


def parseSQLCreateTableAs(sql=[], sqlfile=""):
    # 获取创建的表名
    result = re.sub(r"\s?create\s?table\s?", "", " ".join(sql), 0, re.IGNORECASE)
    result1 = re.sub(r"\s?as.*", "", result, 0, re.IGNORECASE)
    result2 = re.sub(r";", "", result1, 0, re.IGNORECASE)
    colorlog.info("记录下获取的create 表名")
    colorlog.info(result2)
    fromtables = __detachFrom(sql=sql)
    fromtables = [x for x in fromtables if x != 'thename' and x != '']
    colorlog.info("探测当前SQL用到的表:")
    colorlog.info(fromtables)
    # 排重操作
    # 开始维护数据关系
    __packDataStruce(byname=result2, fromtables=fromtables, sqlfile=sqlfile)


def parseSQLInsertInto(sql=[], sqlfile=""):
    """parse SQLLINE with pattern drop table ....
    :param sql: the words array of SQLLINE
    :param sqlfile: SQLLINE IN SQLFILE
    """

    colorlog.info("开始解析insert into 语句{asql}".format(asql=" ".join(sql)))
    result = re.sub(r"\s?insert\s?into\s?", "", " ".join(sql), 0, re.IGNORECASE)
    result1 = re.sub(r"\s?as.*", "", result, 0, re.IGNORECASE)
    result2 = re.sub(r";", "", result1, 0, re.IGNORECASE)
    colorlog.info("表名开始以及后续语句是{thewords}".format(thewords=result2))
    intotablename = result2.split(" ")[0]
    colorlog.info("探测到的表是")
    colorlog.info(intotablename)
    fromtables = __detachFrom(sql=sql)
    fromtables = [x for x in fromtables if x != 'thename' and x != '']
    colorlog.info("查找到的依赖表是{fromtable}".format(fromtable=fromtables))

    __packDataStruce(byname=intotablename, fromtables=fromtables, sqlfile=sqlfile)


def parseSQLSelect(sql=[], sqlfile=""):
    colorlog.info("开始解析select模板语句{asql}".format(asql=" ".join(sql)))
    fromtables = __detachFrom(sql=sql)
    __packDataStruce(byname=None, fromtables=fromtables, sqlfile=sqlfile)


def parseSQLDropTable(sql=[], sqlfile=""):
    """parse SQLLINE with pattern drop table ....
    :param sql: the words array of SQLLINE
    :param sqlfile: SQLLINE IN SQLFILE
    """

    colorlog.info("开始处理drop table 语句")
    result = re.sub(r"\s?drop\s?table\s?", "", " ".join(sql), 0, re.IGNORECASE)
    result1 = re.sub(r"\s?as.*", "", result, 0, re.IGNORECASE)
    result2 = re.sub(r";", "", result1, 0, re.IGNORECASE)
    finaltablename = result2.split(" ")[0]

    colorlog.info("获取到的表名是{tablename}".format(tablename=finaltablename))
    __packDataStruce(byname=finaltablename, fromtables=None, sqlfile=sqlfile)


def __countNumOfItem(theitem, arr):
    count = 0;
    for item in arr:
        if theitem == item:
            count += 1;
    return count


def __putTableIntoScriptDict(tablenames=[], sqlfile=""):
    global scriptTables
    pass
    # 按照SQL文件名存储用到的表
    sqlfilename = sqlfile.split("/")[-1].split(".")[0]
    colorlog.debug(sqlfilename)
    if sqlfilename in scriptTables.keys() and scriptTables[sqlfilename] != None:
        colorlog.info("脚本已经有对应的字典")
        colorlog.info(scriptTables)
        colorlog.info(scriptTables[sqlfilename])
        colorlog.info(tablenames)
        scriptTables[sqlfilename] = scriptTables[sqlfilename] + tablenames
    else:
        scriptTables[sqlfilename] = tablenames


def __processAnoSubQuery(subquery="", tablesforuse=[]):
    colorlog.info("当前语句不存在子查询语法")
    if " on " in subquery:
        colorlog.info("当前语句是一个join on查询")
        countnum = __countNumOfItem("join", subquery.split(" "))
        colorlog.info("一共出现{n}次JOIN连接".format(n=countnum))
        for joinline in subquery.split("join"):
            colorlog.debug("按照join切割后的内容")
            colorlog.debug(joinline)
            result2 = re.sub(r"\s?(join|left\s?join|right\s?join|full\s?join|left|right|full)", "", joinline, 0,
                             re.IGNORECASE)  # 如果多表关联用的是join on 语法
            result3 = re.sub(r"\s+on.*", "", result2, 1, re.IGNORECASE)
            colorlog.info("截取的表部分内容:")
            colorlog.info(result3)
            # 已经拿到了join B on 前的部分
            tablesforuse.append([x for x in re.split(r'(\t|\n|\s|\r)', result3) if x != ' ' and x != ''][0])
    else:
        colorlog.info("当前语法没有on存在,一般连接形式")
        compilerx = re.compile(r"(\s|\n)?[^\s]+(\s)+[^\s]+,")
        line = re.sub(r"\s?where.*", "", subquery, 0, re.IGNORECASE)
        colorlog.info("剔除where后的内容")
        colorlog.info(line)
        if re.match(compilerx, line):
            # 符合多,表名特点
            tablesforuse.append([x for x in re.split(r'(\t|\n|\s|\r)', line) if x != ' ' and x != ''][0])
        else:
            colorlog.info("只用了一个表名")
            colorlog.info(line)
            tablesforuse.append([x for x in re.split(r'(\t|\n|\s|\r)', line) if x != ' ' and x != ''][0])


def __detachFrom(sql=[], tablesforuse=[]):
    if "from" in " ".join(sql):
        # 获取第一个from后的语句
        fromarray = "from".join(" ".join(sql).split("from")[1:])
        colorlog.info("当前语句删除第一个from之后生成的语句如下")
        colorlog.info(fromarray)
        # 并把from中的函数全部替换掉避免出现非必要的逗号
        replacefuntion = re.sub(r"\w+\([^\)]*\)", "thefuntion", fromarray, 0, re.IGNORECASE)
        colorlog.info("把函数体替换后形成的")
        colorlog.info(replacefuntion)

        # 开始判断当前语句是否存在子查询
        if (re.match(r".*\([^\)]*\).*", replacefuntion, re.IGNORECASE)):
            colorlog.info("存在括号体的语法,所以当前语句有子查询")
            subquery = re.findall(r"\([^\)]*\)", replacefuntion, re.IGNORECASE)
            colorlog.info("拿到的括号查询语句是")
            colorlog.info(subquery)

            theleft = re.sub(r"\([^\)]*\)", " thename ", replacefuntion, 0, re.IGNORECASE)
            colorlog.info("剔除()子查询后剩余的字符是")
            colorlog.info(theleft)
            # 替换了子查询后的主体检索
            __processAnoSubQuery(subquery=theleft, tablesforuse=tablesforuse)

            # 逐步查询所有的子查询拿到依赖关系
            # 然后把剩余的子查询循环迭代到本函数中
            for line in subquery:
                __detachFrom(sql=line.split(" "), tablesforuse=tablesforuse)
        else:
            colorlog.info("当前语句不存在子查询语法")
            __processAnoSubQuery(subquery=replacefuntion, tablesforuse=tablesforuse)
    else:
        colorlog.warning("当前需要判断的语句没有子查询,直接被忽略了")
        colorlog.warning(" ".join(sql))

    return [x for x in tablesforuse if x != 'thename' and x != '']


def __packDataStruce(byname="", fromtables=[], sqlfile=""):
    global AllUsedTables
    global AllTableDict
    global scriptTables
    global AllFromTables
    global File_AllUsedTables
    AllUsedTables.append(byname)
    filename = sqlfile.split("/")[-1].split(".")[0]

    if filename in File_AllUsedTables.keys():
        File_AllUsedTables[filename].extend(AllUsedTables)
    else:
        File_AllUsedTables[filename] = AllUsedTables

    if fromtables is None and byname != None:
        __putTableIntoScriptDict(tablenames=[byname], sqlfile=sqlfile)
    elif byname is None and fromtables != None:
        __putTableIntoScriptDict(tablenames=fromtables, sqlfile=sqlfile)
    elif byname != None and fromtables != None and sqlfile != None:
        # 开始维护数据结构
        colorlog.info("开始组建对应的数据结构")
        tableRelations = TableRelations();
        tableRelations.tableName = byname
        tableRelations.tableFroms = list(set(fromtables))
        tableRelations.scriptFiles = sqlfile
        colorlog.info("记录的结构如下:")
        colorlog.info(tableRelations.to_str())

        # 按照表名字存贮关系字典
        if byname in AllTableDict.keys():
            colorlog.error("探测到相同表名重复创建在不同的脚本中")
        else:
            AllTableDict[byname] = tableRelations

        alltablenames = list(set(fromtables))
        alltablenames.append(byname)
        __putTableIntoScriptDict(tablenames=alltablenames, sqlfile=sqlfile)
        AllFromTables.extend(fromtables)

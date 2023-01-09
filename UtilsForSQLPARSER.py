'''
create table as select * from b,c where

'''
import re
from Log import logger

global AllUsedTables;

AllUsedTables=[]

def parseSQLCreateTableAs(sql=[]):
    global AllUsedTables
    pass
    #获取创建的表名
    result=re.sub(r"\s?create\s?table\s?",""," ".join(sql),0,re.IGNORECASE)
    result1=re.sub(r"\s?as.*","",result,0,re.IGNORECASE)
    result2=re.sub(r";","",result1,0,re.IGNORECASE)
    AllUsedTables.append(result2)
    print(result2)
    #获取后面的数据
    result = re.sub(r"\s?create\s?table\s?.*from", "", " ".join(sql), 0, re.IGNORECASE)
    result1=re.sub(r"\s?(where).*", "", result, 0, re.IGNORECASE)#如果多表关联形式的用where 和逗号表示
    print(result1)
    if "on" in sql:
        pass
        #当前出现了join on 语法 探测一共出现了几个join 或者几个on
        countnum=countNumOfItem("join", sql)
        print("一共出现{n}次JOIN连接".format(n=countnum))
        for i in range(0,countnum,1):
            pass
            #按照出现join的次数进行逐次的表名提取
            #然后根据匹配到的数据对生成的语句进行解析
            for joinline in result1.split("join"):
                #print(joinline)
                result2 = re.sub(r"\s?(join|left\s?join|right\s?join|full\s?join|left|right|full)", "", joinline, 0,
                                 re.IGNORECASE)  # 如果多表关联用的是join on 语法
                result3 = re.sub(r"on.*", "", result2, 1, re.IGNORECASE)
                AllUsedTables.append([x for x in re.split(r'(\t|\n|\s|\r)', result3) if x !=' ' and x != ''][0])
    else:
        pass
        #非join方式用表
        #采用逗号
        print("没有采用JOIN连接,把FROM后的表名摘入清单")
        #判断是否是多表
        compilerx=re.compile(r"(\s|\n)?[^\s]+(\s)+[^\s]+,")
        if re.match(compilerx,result1):
            pass
            #符合多,表名特点
            print("多表名逗号关联操作")
            for splitsql in result1.split(","):
                #print(splitsql)
                AllUsedTables.append([x for x in re.split(r'(\t|\n|\s|\r)', splitsql) if x != ' ' and x != ''][0])
        else:
            pass
            print("只用了一个表名")
            AllUsedTables.append([x for x in re.split(r'(\t|\n|\s|\r)', result1) if x !=' ' and x != ''][0])
    #排重操作
    AllUsedTables=list(set(AllUsedTables))

    print(AllUsedTables)


def countNumOfItem(theitem,arr):
    count=0;
    for item in arr:
        if theitem==item:
            count+=1;
    return count

def detachFromTableNameFromSubQuery(sqlline):
    pass

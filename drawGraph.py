import logging
import random
import colorlog
from diagrams import Diagram, Cluster, Edge
from diagrams.programming.flowchart import Database
from UtilsForSQLPARSER import AllUsedTables, AllTableDict, AllFromTables,File_AllUsedTables

colorlog.basicConfig(level=logging.info)

NodeDict={}

RelationArr={}

OnlyOnceList=[]

cluserarrdict={}

def draw():
    global AllUsedTables
    AllUsedTables=list(set(AllUsedTables))
    colorlog.info(AllUsedTables)
    with Diagram("表关系依赖图", show=False, outformat=["jpg", "png", "dot", "svg"],direction="TB"):
        parentNode = Database("Root")
        NodeDict['Root']=parentNode
        with Cluster("Root源"):
            Agroup=[]
            for filename,allusedtable in File_AllUsedTables.items():
                with Cluster("脚本:"+filename+".sql"):
                    filegroup=[]
                    for index, rela in enumerate(AllUsedTables):
                        if rela !=None:
                            __drawANode(tableName=rela, parentNode=parentNode, sqlfile="", thegroup=Agroup, parentNodeName="Root",filegroup=filegroup)


def __drawANode(tableName="", parentNode=None, color="black", sqlfile="", thegroup=[], parentNodeName="",filegroup=[]):
    '''
    :param tableName: 需要判断的节点表名字
    :param parentNode: 父级节点
    :param color:  绘制的颜色
    :param sqlfile: 脚本文件名字
    :param thegroup: 当节点启动一个分组后,分组就是一个数组,所以当前节点应该放进这个分组中
    :param parentNodeName: 父级别的节点表名
    :return: 本方法不返回任何内容
    '''
    thenode=None;
    #通过当前表明是否已经存在绘制节点决定是否重新创建节点还是沿用上一个

    if tableName=="" or tableName==None:
        colorlog.info(tableName)
        colorlog.error("出现了空表名")

    if tableName in NodeDict.keys():
        thenode=NodeDict[tableName]

    else:
        thenode = Database(tableName)

    thegroup.append(thenode)

    NodeDict[tableName] = thenode

    __drawRelation(come=parentNode, to=thenode, filename=sqlfile, comename=parentNodeName, toname=tableName,color=color)

    if tableName not in OnlyOnceList:

        OnlyOnceList.append(tableName) #当前表不再进行迭代循环

        if tableName in AllTableDict.keys():
            colorlog.info("探测到当前表名下有依赖的层级,开始按照来源逐一解析")
            thecolor = __random_color()
            with Cluster(tableName+"源") as newgroup:
                filegroup.append(newgroup)
                Agroup=[]
                for thetablename in AllTableDict[tableName].tableFroms:
                    __drawANode(tableName=thetablename, parentNode=thenode, color=thecolor, sqlfile=AllTableDict[tableName].scriptFiles, thegroup=Agroup, parentNodeName=tableName)
        else:
            colorlog.info("{atablename}当前表已经到了根节点".format(atablename=tableName))
    else:
        colorlog.info("已经探测过的表不再测试")

def __random_color():
    hexadecimal = ["#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])]
    return "".join(hexadecimal)


def __drawRelation(come=None,to=None,filename="",comename="",toname="",defaultoperator="<",color=None):
    '''
        :param come 来方向的节点
        :param to 去方向的节点
        :param filename 对应的连接线上标记的脚本文件名
        :param comename 对应的来方向节点的名字
        :param toname 对应去方向的节点
        :return 返回内容为空,直接参与绘图
    '''

    wetherdraw=True
    #判断当前的绘制关系是否已经存在
    if comename in RelationArr.keys() :
        if toname in RelationArr[comename] :
            colorlog.info("当前的绘制关系已经存在无需再次绘制")
            wetherdraw=False
        else:
            RelationArr[
                comename].append(toname)
    else:
        RelationArr[comename] = [toname]

    if wetherdraw:
        colorlog.debug("开始绘制图形")
        if come == NodeDict['Root']:
            if toname in AllFromTables:
                colorlog.info("当前表明在root节点下,但是在依赖结构中发现他有依赖关系,所以忽略")
            else:
                come - to
        else:
            #come << Edge(color=color, label=filename.split("/")[-1]) << to
            come << Edge(color=color, label=" ") << to
import random

from diagrams import Diagram, Cluster, Edge
from diagrams.programming.flowchart import  Delay,Database

from diagrams.digitalocean.database import DbaasPrimaryStandbyMore, DbaasPrimary, DbaasReadOnly, DbaasStandby
from UtilsForSQLPARSER import AllUsedTables,AllTableDict,scriptTables
from Log import logger
def drawdemo():
    with Diagram("表关系依赖图", show=False, outformat=["jpg", "png", "dot", "svg"],direction="TB"):
        with Cluster("fromcluser"):
            svc_group = [DbaasPrimary("web1"),
                         DbaasPrimary("web2"),
                         DbaasPrimary("web3")]
        [DbaasPrimary("lb"), DbaasPrimary("rb")] << DbaasPrimary("web") >> DbaasPrimary("userdb") >> svc_group >> Edge(
            color="black", style="bold",label="使用SQL脚本") >>DbaasPrimary("web3")

NodeDict={}


def draw():
    with Diagram("表关系依赖图", show=False, outformat=["jpg", "png", "dot", "svg"],direction="TB"):
        parentNode = Database("Root")
        NodeDict['Root']=parentNode
        for index, rela in enumerate(AllUsedTables):
            drawANode(tableName=rela, parentNode=parentNode,sqlfile="")


def drawANode(tableName="",parentNode=None,color="black",sqlfile=""):
    theNode=None;
    if tableName in NodeDict.keys():
        theNode=NodeDict[tableName]
    else:
        theNode = Database(tableName)
        if parentNode == NodeDict['Root']:
            parentNode - theNode
        else:
            parentNode <<Edge(
            color=color,label=sqlfile.split("/")[-1])<<theNode
        NodeDict[tableName]=theNode
    if tableName in AllTableDict.keys():
        logger.info("探测到当前表名下有依赖的层级,开始按照来源逐一解析")
        thecolor = random_color()
        for thetablename in AllTableDict[tableName].tableFroms:
            drawANode(tableName=thetablename, parentNode=theNode,color=thecolor,sqlfile=AllTableDict[tableName].scriptFiles)
    else:
        logger.info("{atablename}当前表已经到了根节点".format(atablename=tableName))

def random_color():
    hexadecimal = ["#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])]
    print("A Random color is :", hexadecimal)
    return "".join(hexadecimal)
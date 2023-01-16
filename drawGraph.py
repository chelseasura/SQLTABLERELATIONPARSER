from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, ECS
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

from diagrams.digitalocean.database import DbaasPrimaryStandbyMore, DbaasPrimary, DbaasReadOnly, DbaasStandby
from UtilsForSQLPARSER import AllUsedTables,AllTableDict,scriptTables
from Log import logger
def drawdemo():
    with Diagram("表关系依赖图", show=False, outformat=["jpg", "png", "dot", "svg"]):
        with Cluster("fromcluser"):
            svc_group = [DbaasPrimary("web1"),
                         DbaasPrimary("web2"),
                         DbaasPrimary("web3")]
        [DbaasPrimary("lb"), DbaasPrimary("rb")] << DbaasPrimary("web") >> DbaasPrimary("userdb") >> svc_group >> Edge(
            color="black", style="bold",label="使用SQL脚本") >>DbaasPrimary("web3")

def draw():
    with Diagram("表关系依赖图", show=False, outformat=["jpg", "png", "dot", "svg"]):
        parentNode = DbaasPrimary("Root")
        for rela in AllUsedTables:
            drawANode(tableName=rela,parentNode=parentNode)

def drawANode(tableName="",parentNode=None):
    newNode = DbaasPrimary(tableName)
    parentNode >> newNode
    if tableName in AllTableDict.keys():
        logger.info("探测到当前表名下有依赖的层级,开始按照来源逐一解析")
        for thetablename in AllTableDict[tableName].tableFroms:
            drawANode(tableName=thetablename, parentNode=newNode)
    else:
        logger.info("当前表已经到了根节点")
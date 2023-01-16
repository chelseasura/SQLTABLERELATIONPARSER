from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, ECS
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

from diagrams.digitalocean.database import DbaasPrimaryStandbyMore, DbaasPrimary, DbaasReadOnly, DbaasStandby


def draw():
    with Diagram("表关系依赖图", show=False, outformat=["jpg", "png", "dot", "svg"]):
        with Cluster("fromcluser"):
            svc_group = [DbaasPrimary("web1"),
                         DbaasPrimary("web2"),
                         DbaasPrimary("web3")]
        [DbaasPrimary("lb"), DbaasPrimary("rb")] << DbaasPrimary("web") >> DbaasPrimary("userdb") >> svc_group >> Edge(
            color="black", style="bold",label="使用SQL脚本") >>DbaasPrimary("web3")

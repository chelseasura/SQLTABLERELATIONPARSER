"""_summary_
   树结构定义的存储结构
   将依赖关系和表名记录在本类中
   
"""

'''
    通过存储的路径列表字典最终维护遍历所有的关联关系
'''


class Node:
    
    pass
    
    level=0 #当前节点所在层级
    
    tableName="" #特指当前节点存储的表名
    
    subNodes=[] #当前节点下的所有子节点
    
    parentNode=[] #当前节点的父节点  因为一张表的来源可能是多张表 所以这是网状结构
    
    NodePath=""  #这是一个字符串标记的路径 /root/2/3/4 类似的一个构建图

class TreeStore:
    
    nodestore=Node();#创建一个Root节点存储
    
    pathdict={}  #全局存储的所有表名和所在地址路径

    def getInstance():
        pass
        treestore=TreeStore()
        
        rootNode=Node()
        rootNode.parentNode=None
        rootNode.NodePath="/Root"
        rootNode.level=1
        rootNode.tableName="None"
        
        treestore.nodestore=rootNode
        treestore.pathdict['Root']=rootNode.NodePath
        
        return treestore


    
if __name__=="__main__":
    pass
    print("单元测试")
    
    treeStore=TreeStore.getInstance()
    print(treeStore.pathdict)
    print(treeStore.nodestore.parentNode)
    

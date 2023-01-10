from optparse import OptionParser

from FileTools import walkpythonfiles

if __name__ == '__main__':
    usage = '''
    这是一个通过解读SQL文件并生成对应的表直接的依赖关系的工具
    usage: -p <path_name> [-u <username> -log <info> ]  
    '''
    parser = OptionParser(usage)

    parser.add_option("-p", "--path_name", dest="path_name", help="输入需要解析对应的目录")
    parser.add_option("--log", "--log", dest="info", help="按照输入参数调整日志级别")
    (options, args) = parser.parse_args()

    if options.path_name :
        # do something
        print("开始解析当前目录{path}下的所有SQL文件,并构建完整的表关系结构图".format(path=options.path_name))
        walkpythonfiles(filepath=options.path_name)
    else:
        print("请输入完整的程序运行参数")
        print(usage)

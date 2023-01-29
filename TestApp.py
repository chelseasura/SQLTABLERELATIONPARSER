import re
import sys

if __name__=="__main__":
    pass
    # s=" ctis_txn_tif_bas_p partition for (to_date('&1','YYYYMMDD')) a"
    # print(s)
    # compilere=re.compile(r"(\s|\n)?[^\s]+(\s)+[^\s]+,")
    # matched=re.match(compilere,s)# 任意空格或者回车出现或者没有 +任意非空格的字符出现多次+出现至少一个空格+任意一个单词出现+至少要出现一个逗号
    # print(matched)
    # s1="v3_1_issu@card a,green2_card_res b,grxxzl_20200803 c" #多表关联
    # print(re.match(compilere,s1))
    # s2 = "v3_1_issu@card a,green2_card_res ,grxxzl_20200803 c,(select 2 from dual)"  # 用到子查询
    # print(re.match(compilere, s2))
    # s3="ctis_txn_tif_bas_p partition for (to_date('&1','YYYYMMDD')) a"
    # print(re.match(compilere, s3))
    #
    # s4=['insert', 'into', 'dqa_lszh_result_0715', '(cust_id,actioncode,val1,val2,val3,accdate)', 'select', 'distinct', "a.cust_id,'1'", 'actioncode,a.开卡日期,a.注册日期,case', 'when', 'a.注册日期', 'is', 'not', 'null', 'then', "'1'", 'else', 'end', "val3,'&1'", 'accdate', 'from', 'green2_card_res', 'a', 'where', 'a.注册日期', 'is', 'not', 'null', 'and', 'a.cust_id', 'not', 'in', '(select', 'b.cust_id', 'from', 'dqa_lszh_result_0620', 'b', 'where', "b.actioncode='1');"]
    # print(" ".join(s4))
    # print(re.sub("(?m)^(?!.*\b(?:invokername=from|insert)\b).*$", "", " ".join(s4), 1, re.IGNORECASE) )

    s5= '''
insert into dqa_lszh_result_0715 (cust_id,actioncode,val1,val2,val3,accdate) select distinct a.cust_id,'8' actioncode,a.开卡日期,b.数据日期,b.公交次数,'&1' accdate from (select a.数据日期,a.客户号,sum(a.bocnet系统交易笔数) 公交次数 from sj_all a where a.数据日期='&1' and a.交易类型='西宁公交' group by a.数据日期,a.客户号)b,  green2_card_res a where a.客户号=b.客户号;
 '''

    #截取from后语句
    # sqlfrom="from".join(s5.split("from")[1:])
    # print(sqlfrom)
    # #并把from中的函数全部替换掉避免出现非必要的逗号
    # replacefuntion=re.sub(r"\w+\([^\)]*\)","thefuntion",sqlfrom,0,re.IGNORECASE)
    # print(replacefuntion)
    #
    # if(re.match(r".*\([^\)]*\).*",replacefuntion,re.IGNORECASE)):
    #     print("剩余的结果是字查询构成的")
    #     subquery=re.findall(r".*\([^\)]*\)",replacefuntion,re.IGNORECASE)
    #     theleft=re.sub(r".*\([^\)]*\).*,","",replacefuntion,0,re.IGNORECASE)
    #     for line in subquery:
    #         print(line)
    #
    #     theleft=re.sub(r"\s?where.*","",theleft,0,re.IGNORECASE)
    #     print(theleft.split(" "))
    print(sys.getrecursionlimit())
    print(sys.setrecursionlimit(2000))



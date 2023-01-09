import re

if __name__=="__main__":
    pass
    s=" ctis_txn_tif_bas_p partition for (to_date('&1','YYYYMMDD')) a"
    print(s)
    compilere=re.compile(r"(\s|\n)?[^\s]+(\s)+[^\s]+,")
    matched=re.match(compilere,s)# 任意空格或者回车出现或者没有 +任意非空格的字符出现多次+出现至少一个空格+任意一个单词出现+至少要出现一个逗号
    print(matched)
    s1="v3_1_issu@card a,green2_card_res b,grxxzl_20200803 c" #多表关联
    print(re.match(compilere,s1))
    s2 = "v3_1_issu@card a,green2_card_res ,grxxzl_20200803 c,(select 2 from dual)"  # 用到子查询
    print(re.match(compilere, s2))
    s3="ctis_txn_tif_bas_p partition for (to_date('&1','YYYYMMDD')) a"
    print(re.match(compilere, s3))

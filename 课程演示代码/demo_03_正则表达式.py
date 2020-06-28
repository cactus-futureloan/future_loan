"""regular expression === >> re ===>> 正则表达式"""
import re

# my_str = "xiaolingwangleli"

# match
# match必须从开始位置进行匹配
# TODO:正则表达式通常在匹配方式前加r，r"a\b"
# TODO:正则表达式当中千万不要随便加空格

# print(re.match(r"ling",my_str))
# search
# 可以在任意地方匹配,只会匹配一个
# res = re.search(r"li",my_str)
# print(res.group())
# find_all
# res = re.findall(r"li",my_str)
# print(res)

# . 匹配任意一个字符，除了 \n
# my_str = "xiaolingwangleli"
# res = re.search(r".",my_str)
# print(res)
#
# res = re.search(r"a.",my_str)
# print(res)

# []代表匹配里面的某一个[abc] 表示要么匹配a，要么匹配b，要么匹配c
# res = re.search(r"[oge]",my_str)
# res = re.search(r"[li|wa]",my_str)
# print(res)

# \d 表示匹配一个数字，\D表示匹配一个非数字
my_str = "_xiao@lingggg256wangleli"

res = re.search(r"\d",my_str)
print(res)
res = re.search(r"\D",my_str)
print(res)
# 和\d等价
print(re.search(r"[0-9]",my_str))

# \w:匹配大小写字母、数字和下划线   \W:匹配非单词字符
# print(re.search(r"\w\w\w",my_str))
# print(re.search(r"\W",my_str))

# *：前面字符任意次，0次或者多次
# print(re.search(r".*",my_str))

# +:前面字符，一次或者多次,尽可能多的匹配，贪婪模式
# print(re.search(r"\d+?",my_str))

# ？：匹配前一个字符出现一次或者0次,表示非贪婪模式
# print(re.search(r"\d?",my_str))

# {m}：匹配m次
# print(re.search(r"g{2,}?",my_str))

# {m,n}：匹配m次到n次

# login_data = '{"member_id":"#member_id#","amount":"#amount#"}'
# pattern = r"#.+?#"
# print(re.search(pattern,login_data))
# result = re.sub(pattern,"19876",login_data,count = 1)
# print(result)
# result = re.sub(pattern,"1000",result,count = 1)
# print(result)

# group
# 括号表示分组
# group(0)：表示匹配的字符
# group(1)：除了group(0)以外，表示括号里面的内容，有多少个括号，就有多少个分组
login_data = '{"member_id":"#member_id#","amount":"#amount#"}'
pattern = r"#(.+?)#"
print(re.search(pattern,login_data).group(1))

# Handler.属性的方式访问数据




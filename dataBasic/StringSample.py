# 字符串s1中\t是制表符，\n是换行符
s1 = "\time up \now"
print(s1)
# 字符串s2中没有转义字符，每个字符都是原始含义
s2 = r"\time up \now"
print(s2)

# Python中还允许在\后面还可以跟一个八进制或者十六进制数来表示字符，
# 例如\141和\x61都代表小写字母a，前者是八进制的表示法，后者是十六进制的表示法。
# 另外一种表示字符的方式是在\u后面跟Unicode字符编码，
# 例如\u9a86\u660a代表的是中文“骆昊”.
s1 = "\141\142\143\x61\x62\x63"
s2 = "\u9a86\u660a"
print(s1, s2)

s = "hello"
for x in range(len(s)):
    print(s[x], end="")

import sys

# 解析参数，得到参数值
ini = sys.argv[1]
ini = ini.split("&")
a = ini[0].split("=")[1]
b = ini[1].split("=")[1]
# 计算
res = str(float(a)+float(b))

# 构造html输出
output = ""
with open("cgi-bin/calculator_res.html", "r") as file:
    for line in file:
        output += line
output = output.replace("$op1", a)
output = output.replace("$op2", b)
# 加法
output = output.replace("$res", res)

print(output)

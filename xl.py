str = "a3deepak2"
out = ""
ss = ""
for i in str:
    if i.isdigit():
        ss*=int(i)
        out+=ss
        ss=""
    else:
        ss+=i
print(out)

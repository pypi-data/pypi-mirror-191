def eo(num):
    n=1
    if num<0:
        a="Negative Number"
        return a
    if num>1000000000000000:
        b="Exceeded 100 trillion"
        return b
    if type(num)!=type(n):
        c=f"Type : {type(num)}"
        return c
    else:
        if num==0 or num%2==0:
            d="Even"
            return d
        if num%2==1:
            e="Odd"
            return e
        else:
            f="Unexcepted Error"
            return f
def TypeS(a):
    A=[1,2]
    b=(1,2)
    c="wdqqdq"
    d='asdasd'
    e=1.5
    f=1
    if type(a)==type(A):
        return "List"
    elif type(a)==type(b):
        return "Tuple"
    elif type(a)==type(c) or type(a)==type(d):
        return "String"
    elif type(a)==type(e):
        return "Float"
    elif type(a)==type(f):
        return "Int"
    else:
        return "Unexcepted Type"
def wtxt(filename,file_data):
    with open(filename,'w') as f:
        f.write(file_data)
def atxt(filename,file_data):
    with open(filename,'a') as f:
        f.write(file_data)

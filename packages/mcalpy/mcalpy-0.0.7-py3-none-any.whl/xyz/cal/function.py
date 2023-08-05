from tkinter import *
import math
from os import *
from tkinter.font import *
from sys import argv
F=1
result=0
If=0
II=0
oo="0"
oo1="0"
root=Tk()
E
root.title("Calculator")
root.resizable(True,True)
def sm1(value):
    value=str(value)
    return value[:-1]
try:
    if argv[1] == '-dev' or argv[1] == '-developer':
        FONTS=Font(family="궁서", size=10, slant="roman")
    else:
        FONTS=Font(family="궁서", size=15, slant="roman")
except: FONTS=Font(family="궁서", size=15, slant="roman")
label=Label(root, text=0, relief="solid",width=50,height=5,font=FONTS)
oo=int(oo)
label.grid(row=1,column=2)
mode=1
arg=argv[1:]
def ii(v):
    try:
        v=float(v)
    except:
        return None
    else:
        return v
def PM(f,s):
    global F,Pms,If
    if Pms==2:
        if F==1:
            if If==0:
                return float(str(f[:-1]) + str(s))
            elif If==1:
                return float(str(f) + str(s))
        else:
            return float(str(f) + str(s))
    if Pms==1:
        return int(str(f) + str(s))

def M1():
    global F,If, Pms
    if mode==1:
        global oo
        oo=PM(str(oo), 1)
        if If==0:
            if Pms==2:
                F=1
                If=1
        label.config(text=str(oo), relief="solid")
    else:
        
        global oo1
        oo1=PM(str(oo1), 1)
        if If==0:
            if Pms==2:
                F=1
                If=1
        label.config(text=str(oo1), relief="solid")
        
def M2():
    global F, If, Pms
    if mode==1:
        global oo
        oo=PM(str(oo), 2)
        if If==0:
            if Pms==2:
                F=1
                If=1
        label.config(text=str(oo), relief="solid")
        
    else:
        global oo1
        oo1=PM(str(oo1), 2)
        if If==0:
            if Pms==2:
                F=1
                If=1
        label.config(text=str(oo1), relief="solid")
        
def M3():
    global F, If, Pms
    global oo1,oo
    if mode==1:
        oo=PM(str(oo), 3)
        if If==0:
            if Pms==2:
                F=1
                If=1
        if oo==3141592653589793:
            print('WOW How do you know?')
        label.config(text=str(oo), relief="solid")
        
    else:
        oo1=PM(str(oo1), 3)
        if If==0:
            if Pms==2:
                F=1
                If=1
        if oo1==3141592653589793:
            print('WOW How do you know?')
        label.config(text=str(oo1), relief="solid")
        
def M4():
    global F, If, Pms
    if mode==1:
        global oo
        oo=PM(str(oo), 4)
        if If==0:
            if Pms==2:
                F=1
                If=1
        if oo==10314:
            print('My class!')
        label.config(text=str(oo), relief="solid")
        
    else:
        global oo1
        oo1=PM(str(oo1), 4)
        if If==0:
            if Pms==2:
                F=1
                If=1
        if oo1==10314:
            print('My class!')
        label.config(text=str(oo1), relief="solid")
        
def M5():
    global F, If, Pms
    if mode==1:
        global oo
        oo=PM(str(oo), 5)
        if If==0:
            if Pms==2:
                F=1
                If=1
        label.config(text=str(oo), relief="solid")
        
    else:
        global oo1
        oo1=PM(str(oo1), 5)
        if If==0:
            if Pms==2:
                F=1
                If=1
        label.config(text=str(oo1), relief="solid")
        
def M6():
    global F, If, Pms
    if mode==1:
        global oo
        oo=PM(str(oo), 6)
        if If==0:
            if Pms==2:
                F=1
                If=1
        if oo==90306:
            print('WOW It is my birth day!')
        if oo==6283185307179586:
            print('It is 6.283185307179586, π*2')
        label.config(text=str(oo), relief="solid")
        
    else:
        global oo1
        oo1=PM(str(oo1), 6)
        if If==0:
            if Pms==2:
                F=1
                If=1
        if oo1==90306:
            print('WOW It is my birth day!')
        if oo1==6283185307179586:
            print('It is 6.283185307179586, π*2')
        label.config(text=str(oo1), relief="solid")
        
def M7():
    global F, If, Pms
    if mode==1:
        global oo
        oo=PM(str(oo), 7)
        if If==0:
            if Pms==2:
                F=1
                If=1
        label.config(text=str(oo), relief="solid")
    else:
        global oo1
        oo1=PM(str(oo1), 7)
        if If==0:
            if Pms==2:
                F=1
                If=1
        label.config(text=str(oo1), relief="solid")
        
def M8():
    global II,F, If, Pms
    II=1
    if mode==1:
        if If==0:
            if Pms==2:
                F=1
                If=1
        global oo
        oo=PM(str(oo), 8)
        if oo==20221030235958:
            system('chcp 65001')
            system('cls')
            print('이것은 만든 날짜이고 이 숫자는 제작자의 모든 프로그램의 이스터에그의 숫자 일 겁니다!')
        label.config(text=str(oo), relief="solid")
        
    else:
        if If==0:
            if Pms==2:
                F=1
                If=1
        global oo1
        oo1=PM(str(oo1), 8)
        if oo1==20221030235958:
            system('chcp 65001')
            system('cls')
            print('이것은 만든 날짜이고 이 숫자는 제작자의 모든 프로그램의 이스터에그의 숫자 일 겁니다!')
        label.config(text=str(oo1), relief="solid")
        
def M9():
    global F, If, Pms
    if mode==1:
        if If==0:
            if Pms==2:
                F=1
                If=1
        global oo
        oo=PM(str(oo), 9)
        label.config(text=str(oo), relief="solid")
        
    else:
        
        if If==0:
            if Pms==2:
                F=1
                If=1
        global oo1
        oo1=PM(str(oo1), 9)
        label.config(text=str(oo1), relief="solid")
        
def M0():
    global F, If, Pms
    if mode==1:
        if If==0:
            if Pms==2:
                F=1
                If=1
        global oo
        oo=PM(str(oo), 0)
        label.config(text=str(oo), relief="solid")
    else:
        if If==0:
            if Pms==2:
                F=1
                If=1
        global oo1
        oo1=PM(str(oo1), 0)
        label.config(text=str(oo1), relief="solid")
        
def sf():
    global F
    F=0
def SM():
    global oo,oo1,Pms
    Pms=2
    if mode==1:
        oo=float(oo)
        label.config(text=str(oo), relief="solid")
    else:
        oo1=float(oo1)
        label.config(text=str(oo1), relief="solid")

def Add():
    global mode, choice, Pms, If
    sf()
    mode=2
    If=0
    choice=1
    Pms=1
    label.config(text=0, relief="solid")
def subs():
    sf()
    global mode, choice, Pms, If
    If=0
    mode=2
    Pms=1
    choice=2
    label.config(text=0, relief="solid")
def muls():
    sf()
    global mode, choice, Pms, If
    If=0
    Pms=1
    mode=2
    choice=3
    label.config(text=0, relief="solid")
def divs():
    global mode, choice, Pms, If
    If=0
    sf()
    Pms=1
    mode=2
    choice=4
    label.config(text=0, relief="solid")
def pows():
    global mode, choice, Pms, If
    If=0
    sf()
    Pms=1
    mode=2
    choice=5
    label.config(text=0, relief="solid")
def sqrs():
    global mode, choice, oo, oo1, result, Pms, If
    If=0
    sf()
    Pms=1
    choice=6
    label.config(text=math.sqrt(oo), relief="solid")
    oo=0
    oo1=0
    result=0
def pers():
    global mode, choice, oo, oo1, result, Pms, If
    If=0
    sf()
    Pms=1
    choice=7
    label.config(text=oo/100, relief="solid")
    oo=0
    oo1=0
    result=0
def Abs():
    global mode, oo, oo1
    if mode == 1:
        oo = abs(oo)
        label.config(text=oo, relief='solid')
    else:
        oo1=abs(oo1)
        label.config(text=oo1,relief='solid')
def f():
    global mode, oo, oo1
    if mode == 1:
        oo = math.factorial(oo)
        label.config(text=oo, relief='solid')
    else:
        oo1 = math.factorial(oo1)
        label.config(text=oo1,relief='solid')
def sins():
    global mode, oo, oo1
    if mode == 1:
        oo = math.sin(oo)
        label.config(text=oo, relief='solid')
    else:
        oo1 = math.sin(oo1)
        label.config(text=oo1,relief='solid')
def coss():
    global mode, oo, oo1
    if mode == 1:
        oo = math.cos(oo)
        label.config(text=oo, relief='solid')
    else:
        oo1 = math.cos(oo1)
        label.config(text=oo1,relief='solid')
def tans():
    global mode, oo, oo1
    if mode == 1:
        oo = math.tan(oo)
        label.config(text=oo, relief='solid')
    else:
        oo1 = math.tan(oo1)
        label.config(text=oo1,relief='solid')
def Return():
    global oo1, oo, mode, choice, result, Pms, If
    If=0
    sf()
    Pms=1
    mode=1
    if choice == 1:result=oo+oo1
    elif choice == 2: result= oo-oo1
    elif choice == 3: result= oo*oo1
    elif choice == 4:
        if oo1 != 0: result=oo/oo1
        else: result=oo
    elif choice == 5:result=oo**oo1
    label.config(text=result, relief="solid")
    oo=result
    oo1=0
    result = 0
def clear():
    global oo1, oo, mode, choice, result, Pms, If
    If=0
    Pms=1
    mode = 1
    label.config(text=0, relief="solid")
    oo = 0
    oo1 = 0
    result = 0
def De():
    global oo, oo1, mode
    if mode == 1:
        oo=int((int(oo))/10)
        label.config(text=oo, relief="solid")
    else:
        oo1=int((int(oo1))/10)
        label.config(text=oo1, relief="solid")
def pis():
    global mode, oo, oo1
    if mode == 1:
        oo = math.pi
        label.config(text=oo, relief='solid')
    else:
        oo1 = math.pi
        label.config(text=oo1,relief='solid')
def p2():
    global mode, oo, oo1
    if mode == 1:
        oo = math.tau
        label.config(text=oo, relief='solid')
    else:
        oo1 = math.tau
        label.config(text=oo1,relief='solid')
def pis5():
    label.config(text='3.14159265358979323846264338327950288419716939937510582',relief="solid")
def p25():
    label.config(text='6.28318530717958647692528676655900576839433879875021164',relief="solid")
def e():
    global mode, oo, oo1
    if mode == 1:
        oo = math.exp(oo)
        label.config(text=oo, relief='solid')
    else:
        oo1 = math.exp(oo1)
        label.config(text=oo1,relief='solid')
def p(value):
    print(value)
Pms=1
Or="raised"
button=Button(root, overrelief=Or, text="1",command=M1,repeatinterval=500,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=4,column=1)
button=Button(root, overrelief=Or, text="2",command=M2,repeatinterval=500,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=4,column=2)
button=Button(root, overrelief=Or, text="3",command=M3,repeatinterval=500,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=4,column=3)
button=Button(root, overrelief=Or, text="4",command=M4,repeatinterval=500,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=3,column=1)
button=Button(root, overrelief=Or, text="5",command=M5,repeatinterval=500,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=3,column=2)
button=Button(root, overrelief=Or, text="6",command=M6,repeatinterval=500,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=3,column=3)
button=Button(root, overrelief=Or, text="7",command=M7,repeatinterval=500,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=2,column=1)
button=Button(root, overrelief=Or, text="8",command=M8,repeatinterval=500,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=2,column=2)
button=Button(root, overrelief=Or, text="9",command=M9,repeatinterval=500,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=2,column=3)
button=Button(root, overrelief=Or, text="0",command=M0,repeatinterval=500,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=5,column=2)
button=Button(root, overrelief=Or, text="C",command=clear,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=5,column=1)
button=Button(root, overrelief=Or, text="=",command=Return,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=1,column=1)
button=Button(root, overrelief=Or, text="+",command=Add,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=6,column=1)
button=Button(root, overrelief=Or, text="-",command=subs,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=6,column=2)
button=Button(root, overrelief=Or, text="x",command=muls,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=6,column=3)
button=Button(root, overrelief=Or, text="÷",command=divs,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=7,column=1)
button=Button(root, overrelief=Or, text="^",command=pows,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=7,column=2)
button=Button(root, overrelief=Or, text="√",command=sqrs,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=7,column=3)
button=Button(root, overrelief=Or, text="del",command=De,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=1,column=3)
button=Button(root, overrelief=Or, text="%",command=pers,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=5,column=3)
button=Button(root, overrelief=Or, text="π",command=pis,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=8,column=1)
button=Button(root, overrelief=Or, text="e",command=e, width=50,height=5,font=FONTS,relief="solid")
button.grid(row=8,column=3)
button=Button(root, overrelief=Or, text="τ",command=p2,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=8,column=2)
button=Button(root, overrelief=Or, text=".",command=SM,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=1,column=4)
button=Button(root, overrelief=Or, text="π 1st ~ 53th",command=pis5,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=2,column=4)
button=Button(root, overrelief=Or, text="τ 1st ~ 53th",command=p25,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=3,column=4)
button=Button(root, overrelief=Or, text="abs",command=Abs,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=4,column=4)
button=Button(root, overrelief=Or, text="!",command=f,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=5,column=4)
button=Button(root, overrelief=Or, text="sin",command=sins,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=6,column=4)
button=Button(root, overrelief=Or, text="cos",command=coss,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=7,column=4)
button=Button(root, overrelief=Or, text="tan",command=tans,width=50,height=5,font=FONTS,relief="solid")
button.grid(row=8,column=4)


def ACT() -> int:
    """
    It is GUI calculator
    action way: ACT()
    """
    global root
    root.mainloop()
    return 0
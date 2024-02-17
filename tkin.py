def add():
    a=int(input("Enter first number:"))
    b=int(input("Enter second nuber:"))
    print(a+b)

from tkinter import *
top=Tk()
top.title("Calculator")
top.geometry("500x500")

en=Entry(top,width=10)
en.grid(row=0,column=0,columnspan=4)

clear=Button(top,text="C")
clear.grid(row=1,column=0)

perce=Button(top,text="%")
perce.grid(row=1,column=1)

dot=Button(top,text=".")
dot.grid(row=1,column=2)

div=Button(top,text="/")
div.grid(row=1,column=3)

b9=Button(top,text="9")
b9.grid(row=2,column=2)

b8=Button(top,text="8")
b8.grid(row=2,column=1)

b7=Button(top,text="7")
b7.grid(row=2,column=0)

mul=Button(top,text="x")
mul.grid(row=2,column=3)

b6=Button(top,text="6")
b6.grid(row=3,column=2)

b5=Button(top,text="5")
b5.grid(row=3,column=1)

b4=Button(top,text="4")
b4.grid(row=3,column=0)

sub=Button(top,text="-")
sub.grid(row=3,column=3)

b3=Button(top,text="3")
b3.grid(row=4,column=2)

b2=Button(top,text="2")
b2.grid(row=4,column=1)

add=Button(top,text="+",command=add)
add.grid(row=4,column=3)
#add=top.Button(top, command=add)

b1=Button(top,text="1")
b1.grid(row=4,column=0)

b0=Button(top,text="0")
b0.grid(row=5,column=1)

op=Button(top,text="(")
op.grid(row=5,column=0)

cp=Button(top,text=")")
cp.grid(row=5,column=2)

eq=Button(top,text="=")
eq.grid(row=5,column=3)

top.mainloop()

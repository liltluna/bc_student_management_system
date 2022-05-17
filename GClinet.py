from tkinter import *
from socket import *


class mesage:
    def __init__(self,aut,name,ps):
        pass
            


class client:
    def __init__(self,ip,post) :
        self.ip=ip                        #绑定IP
        self.post=post                    #端口
        self.authority=0                  #权限等级，会根据用户的选择而改变
        self.name_E=Entry()               #用户名输入框
        self.ps_E=Entry(show='*')         #密码输入框
        self.bt=Button()                  #确定按钮
    def Login(self) :
        #self.top.geometry('+10+10')
        '''登录页面，由用户选择权限，
           输入用户名和密码，按钮的监听函数待完善'''
        
        #权限选择
        M=StringVar(self.top)
        M.set('权限')
        om=OptionMenu(self.top,M,'A','B','V')
        om.grid(row=0,column=1)

        #用户输入框
        name_M=Message()
        name_M['text']='用户'
        name_M.grid(row=1,column=0)
        self.name_E.grid(row=1,column=1)


        #密码输入框
        ps_M=Message()
        ps_M['text']='密码'
        ps_M.grid(row=2,column=0)
        self.ps_E.grid(row=2,column=1) 

        self.bt['text']='确定'
        self.bt.grid(row=3,column=0)

        bt2=Button(text='取消').grid(row=3,column=2)
        
        #self.top['menu']=self.M
        pass
    def show(self):
        '''判断权限，根据权限执行不同的内容，显示不同的页面
            ，具体执行内容待完善'''
        if self.authority==1:
            pass
        elif self.authority==2:
            pass
        elif self.authority==3:
            pass
    def communicate(self,st):
        '''通讯函数，负责与服务器进行沟通，
           ip与端口在创建类时进行指定，
           st表示要传输的内容'''
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((self.ip,self.post))
        pass

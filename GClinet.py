from tkinter import *
from tkinter import ttk
from socket import *
from HandleProcess import *

class mesage:
    def __init__(self,aut,name,ps):
        pass
            


class client:
    def __init__(self) :
       ###登陆与注册界面需要用的组件
        self.top=Tk()                      #端口
        self.top.geometry('800x600')
    
        self.fm1=Frame(self.top)           #登陆页面
        self.fm2=Frame(self.top)           #注册页面
        self.fm3=Frame(self.top)           #登录后的显示页面
        self.opera='l'
        self.authority=0                   #权限等级，会根据用户的选择而改变
        self.name=''                       #用户名输入框
        self.ps=''                         #密码输入框
        
        
    def Login(self) :
        
        '''登录页面，由用户选择权限，
           输入用户名和密码，按钮的监听函数待完善'''
        
        self.top.title('python分组管理系统')
        canvas_root = Canvas(self.fm1, width=800, height=600)
        im_root = HP.get_img('bj.png',800, 600)
        canvas_root.create_image(400, 300, image=im_root)
        canvas_root.pack()

        self.fm1.pack()
        
        #权限选择
        M=StringVar(self.fm1)
        M.set('权限')
        om=ttk.Combobox(self.fm1,textvariable=M,values=['一般用户','组长','教师'],state='readonly')
        om.bind('<<ComboboxSelected>>',lambda event:self.Change_Authority(event,om.get()))
        om.place(x=625,y=200)
               
        
        #用户输入框
        name_E=Entry(self.fm1)
        name_M=Message(self.fm1)
        name_M['text']='用户'
        name_M.place(x=600,y=250)
        name_E.place(x=650,y=250)


        #密码输入框
        ps_E=Entry(self.fm1,show='*')
        ps_M=Message(self.fm1)
        ps_M['text']='密码'
        ps_M.place(x=600,y=300)
        ps_E.place(x=650,y=300)
        bt=Button(self.fm1,text='确定',command=self.View)
        
        bt.place(x=675,y=350)

        btR=Button(self.fm1,text='没有账号？点这里创建！',command=self.Regist).place(x=625,y=400)
        
        
        self.top.mainloop()
        pass
    def Regist(self) :
        self.fm1.pack_forget()

        canvas_root = Canvas(self.fm2, width=800, height=600)
        im_root = HP.get_img('bj.png',800, 600)
        canvas_root.create_image(400, 300, image=im_root)
        canvas_root.pack()

        self.fm2.pack()
        name_E=Entry(self.fm2)               #姓名输入框
        stu_E=Entry(self.fm2)                #学号输入框
        ps_E=Entry(self.fm2,show='*')         #密码输入框
        authority=0

        M=StringVar(self.fm2)
        M.set('权限')
        om=ttk.Combobox(self.fm1,textvariable=M,values=['一般用户','组长','教师'],state='readonly')
        om.bind('<<ComboboxSelected>>',lambda event:self.Change_Authority(event,om.get()))
        om.place(x=625,y=200)

   
        name_M=Message(self.fm2,text='姓名')
        stu_M=Message(self.fm2,text='学号/工号')
        ps_M=Message(self.fm2,text='密码')

        name_E.place(x=650,y=250)
        stu_E.place(x=650,y=300)
        ps_E.place(x=650,y=350)        
        name_M.place(x=600,y=250)
        stu_M.place(x=585,y=300)
        ps_M.place(x=600,y=350)
        bt1=Button(self.fm2,text='确定',command=self.View).place(x=650,y=400)
        bt2=Button(self.fm2,text='取消',command=self.back).place(x=725,y=400)
        self.top.mainloop()

    def View(self):
        self.fm1.pack_forget()
        self.fm2.pack_forget()
        self.fm3.pack(fill=BOTH,expand=1)


        canvas_root = Canvas(self.fm3, width=800, height=600)
        im_root = HP.get_img('bj.png',800, 600)
        canvas_root.create_image(400, 300, image=im_root)
        canvas_root.pack()

        
        wel=Message(self.fm3,foreground='green',text='欢迎使用python用户管理系统',aspect=800)
        name_M=Message(self.fm3,text='姓名:')
        stu_M=Message(self.fm3,text='工号:')

        name=Message(self.fm3,text='yjc')
        stu=Message(self.fm3,text='2020211723',aspect=800)

        wel.place(x=325,y=25)
        name_M.place(x=250,y=100)
        name.place(x=350,y=100)
        stu_M.place(x=250,y=150)
        stu.place(x=350,y=150)

        
        Mission_N=['a','b','c']
        Mission_F=[]

        
        M_N=ToggledFrame(self.fm3,text='当前的任务',width=200,height=30)
        for con in Mission_N:
            ttk.Label(M_N.sub_frame, text=con).pack()
        
        
        M_N.place(x=300,y=400)

        
        M_F=ToggledFrame(self.fm3,text='已完成任务',width=200,height=30)
        for con in Mission_F:
            ttk.Label(M_F.sub_frame, text=con).pack()
       
        M_F.place(x=450,y=400)
        if self.authority==1:
            '''普通组员'''
            ssbj=Message(self.fm3,text='所属班级')
            ssxz=Message(self.fm3,text='所属小组')
            ssbj.place(x=250,y=200)
            ssxz.place(x=250,y=250)
        if self.authority==2:
            '''组长'''
            ssbj=Message(self.fm3,text='所属班级')
            glxz=Message(self.fm3,text='管理小组')
            glmd=ToggledFrame(self.fm3,text='管理名单',width=300,height=30)
           # glmd.pack_propagate(0)
            ssbj.place(x=250,y=200)
            glxz.place(x=250,y=250)
            glmd.place(x=375,y=300)
            pass
        if self.authority>=3:
            '''授课老师'''
            glbj=Message(self.fm3,text='管理班级')
            xzmd=ToggledFrame(self.fm3,text='小组名单',width=300,height=30)
            glbj.place(x=250,y=200)
            #xzmd.pack_propagate(0)
            xzmd.place(x=375,y=300)
            pass


        self.top.mainloop()
    def back(self):
        self.fm1.pack()
        self.fm2.pack_forget()
    def Show(self):
        '''判断权限，根据权限执行不同的内容，显示不同的页面
            ，具体执行内容待完善'''
        if self.authority==1:
            pass
        elif self.authority==2:
            pass
        elif self.authority==3:
            pass
    def Change_Authority(self,event,n):
         if n=='一般用户':
             self.authority=1
         elif n=='组长':
             self.authority=2
         elif n=='教师':
             self.authority=3
        
    def communicate(self,st):
        '''通讯函数，负责与服务器进行沟通，
           ip与端口在创建类时进行指定，
           st表示要传输的内容'''
        ip=''
        post=''
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((ip,post))
        pass
    
         
c=client()
c.Login()

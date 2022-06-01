import pickle
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from socket import *
from HandleProcess import *
from GPacket import *
from GUser import *


class client:
    def __init__(self):
        # 登陆与注册界面需要用的组件
        self.top = Tk()  # 端口
        self.top.geometry('1600x900')

        self.fm1 = Frame(self.top)  # 登陆页面
        self.fm2 = Frame(self.top)  # 注册页面
        self.fm3 = Frame(self.top)  # 登录后的显示页面
        self.opera = 'l'
        self.authority = 0  # 权限等级，会根据用户的选择而改变，登陆时需核对
        self.name = ''  # 用户名输入框，登陆时需核对
        self.ps = ''  # 密码输入框，登陆时需核对

        HOST = 'B-Altair'  # 使用的时候修改成服务器对应的名称
        PORT = 8888

        self.ADDR = (HOST, PORT)
        self.tcpCliSock = socket(AF_INET, SOCK_STREAM)

    def set_user_name(self, n):
        self.name = n

    def set_password(self, ps):
        self.ps = ps

    def get_user_name(self):
        return self.name

    def Log_check(self):

        try:
            self.tcpCliSock.connect(self.ADDR)
        except:
             messagebox.askokcancel(title='提示', message='连接失败，请检查你的网络')
        else:
            self.Login()

    def Login(self):

        ''' 选择权限，输入用户名和密码'''

        self.top.title('python分组管理系统')
        canvas_root = Canvas(self.fm1, width=1600, height=900)
        im_root = HP.get_img('bj.png', 1600, 900)
        canvas_root.create_image(800, 450, image=im_root)
        canvas_root.pack()

        self.fm1.pack()

        # 权限选择
        M = StringVar(self.fm1)
        M.set('权限')
        om = ttk.Combobox(self.fm1, textvariable=M, values=['一般用户', '组长', '教师'], state='readonly')
        om.bind('<<ComboboxSelected>>', lambda event: self.Change_Authority(event, om.get()))
        om.place(x=625, y=200)

        # 用户输入框
        name_E = Entry(self.fm1)
        name_M = Message(self.fm1)
        name_M['text'] = '用户'
        name_M.place(x=600, y=250)
        name_E.place(x=650, y=250)

        # 密码输入框
        ps_E = Entry(self.fm1, show='*')
        ps_M = Message(self.fm1)
        ps_M['text'] = '密码'
        ps_M.place(x=600, y=300)
        ps_E.place(x=650, y=300)
        bt = Button(self.fm1, text='确定', command=lambda: self.View(name_E.get(), ps_E.get()))

        bt.place(x=675, y=350)

        btR = Button(self.fm1, text='没有账号？点这里创建！', command=self.Regist).place(x=625, y=400)

        self.top.mainloop()
        pass

    def Regist(self):
        '''注册页面，目前还需要一个完善信息的页面，等待设计'''

        self.fm1.pack_forget()

        canvas_root = Canvas(self.fm2, width=1600, height=900)
        im_root = HP.get_img('bj.png', 1600, 900)
        canvas_root.create_image(800, 450, image=im_root)
        canvas_root.pack()

        self.fm2.pack()
        name_E = Entry(self.fm2)  # 姓名输入框
        stu_E = Entry(self.fm2)  # 学号输入框
        ps_E = Entry(self.fm2, show='*')  # 密码输入框
        authority = 0

        M = StringVar(self.fm2)
        M.set('权限')
        om = ttk.Combobox(self.fm1, textvariable=M, values=['一般用户', '组长', '教师'], state='readonly')
        om.bind('<<ComboboxSelected>>', lambda event: self.Change_Authority(event, om.get()))
        om.place(x=625, y=200)

        name_M = Message(self.fm2, text='用户名')
        stu_M = Message(self.fm2, text='学号/工号')
        ps_M = Message(self.fm2, text='密码')

        name_E.place(x=650, y=250)
        stu_E.place(x=650, y=300)
        ps_E.place(x=650, y=350)
        name_M.place(x=600, y=250)
        stu_M.place(x=585, y=300)
        ps_M.place(x=600, y=350)
        Button(self.fm2, text='确定',
               command=lambda: self.Regist_check(name_E.get(), stu_E.get(), ps_E.get())).place(x=650, y=400)
        Button(self.fm2, text='取消', command=self.back).place(x=725, y=400)
        self.top.mainloop()

    def View(self, name_g, ps_g):

        """判断权限，根据权限执行不同的内容，显示不同的页面
        """
        self.set_user_name(name_g)
        self.set_password(ps_g)

        GM = GUser.GroupMember()
        GM.setUser_name(self.name)
        GM.setPassword(self.ps)
        GM.setUser_type(self.authority)

        operator = Packet_operate()
        operator.setOperator(GM)
        packet1 = Packet_login()  # 登陆请求
        packet2 = Packet_search_info(operator)  # 查询请求

        res1 = self.communicate(packet1)
        res2 = self.communicate(packet2)

        if not res1 or not res2:
            messagebox.askokcancel(title='提示', message='找不到对象')
            exit(0)
        
        self.fm1.pack_forget()
        self.fm2.pack_forget()
        self.fm3.pack()

        canvas_root = Canvas(self.fm3, width=1600, height=900)
        im_root = HP.get_img('bj.png', 1600, 900)
        canvas_root.create_image(800, 450, image=im_root)
        canvas_root.pack()

        wel = Message(self.fm3, foreground='green', text='欢迎使用python用户管理系统', aspect=800)
        name_M = Message(self.fm3, text='姓名:')
        stu_M = Message(self.fm3, text='学号:')

        name = Message(self.fm3, text=res2[0][0])
        stu = Message(self.fm3, text=res2[0][2], aspect=800)

        wel.place(x=650, y=50)
        name_M.place(x=500, y=200)
        name.place(x=700, y=200)
        stu_M.place(x=500, y=300)
        stu.place(x=700, y=300)

        M_N = ToggledFrame(self.fm3, text='管理结果', width=200, height=30)

        M_N.place(x=450, y=550)

        if self.authority == 1:
            '''普通组员'''
            ssbj = Message(self.fm3, text='所属班级')
            ssxz = Message(self.fm3, text='所属小组')
            ssbj_M=Message(self.fm3,text='2020211317')
            ssxz_M=Message(self.fm3,text=res2[0][3])

            ssbj.place(x=500, y=400)
            ssxz.place(x=500, y=500)
            ssbj_M.place(x=700,y=400)
            ssxz_M.place(x=700,y=500)
        if self.authority == 2:
            '''组长'''
            ssbj = Message(self.fm3, text='所属班级')
            glxz = Message(self.fm3, text='管理小组')
            glxz_M=Message(self.fm3,text=res2[0][3])
            ssbj_M=Message(self.fm3,text='2020211317')
            ssbj.place(x=500, y=400)
            glxz.place(x=500, y=500)
            ssbj_M.place(x=700,y=400)
        if self.authority >= 3:
            '''授课老师'''
            glbj = Message(self.fm3, text='管理班级')
            glbj_M=Message(self.fm3,text='2020211317')
            glbj.place(x=500, y=400)
            glbj_M.place(x=700,y=400)

        tree = ttk.Treeview(M_N.sub_frame, columns=(
            'name', 'sex', 'student_number', 'group_number', 'qq_number', 'user_type', 'password', 'username'),
                            show="headings", displaycolumns="#all")

        tree.column('name', width=80)
        tree.column('sex', width=50)
        tree.column('student_number', width=100)
        tree.column('group_number', width=100)
        tree.column('qq_number', width=100)
        tree.column('user_type', width=50)
        tree.column('password', width=100)
        tree.column('username', width=100)

        tree.heading('name', text="姓名", anchor=W)
        tree.heading('sex', text="性别", anchor=W)
        tree.heading('student_number', text="学号", anchor=W)
        tree.heading('group_number', text="小组编号", anchor=W)
        tree.heading('qq_number', text="QQ号", anchor=W)
        tree.heading('user_type', text="用户等级", anchor=W)
        tree.heading('password', text="密码", anchor=W)
        tree.heading('username', text="用户名", anchor=W)

        def deljob():
            '''view界面的删除命令'''
            iid = tree.selection()
            packet = Packet_delete_info()
            packet.setOperator(operator)
            d = tree.item(tree.focus())
            delee = GUser.GroupMember()
            delee.setStuent_number(d['student_number'])
            packet.setDelete_info(delee)
            self.communicate(packet)

            tree.delete(iid)

        def addjob():
            '''view界面的增加命令'''
            add = Tk()
            name_M = Message(add, text='姓名')
            name = Entry(add)
            sex_M =Message(add, text='性别')
            sex = ttk.Combobox(add,  values=['M','F'], state='readonly')
            name_M.grid(row=0, column=0)
            name.grid(row=0, column=1)
            sex_M.grid(row=1, column=0)
            sex.grid(row=1, column=1)

            stu_M = Message(add, text='学号')
            stu = Entry(add)
            gro_M = Message(add, text='所属小组')
            gro = Entry(add)
            stu_M.grid(row=2, column=0)
            stu.grid(row=2, column=1)
            gro_M.grid(row=3, column=0)
            gro.grid(row=3, column=1)

            ut_M = Message(add, text='用户等级')
            ut  = ttk.Combobox(add, values=['一般用户','组长','教师'], state='readonly')
            ps_M = Message(add, text='密码')
            ps = Entry(add)
            ut_M.grid(row=4, column=0)
            ut.grid(row=4, column=1)
            ps_M.grid(row=5, column=0)
            ps.grid(row=5, column=1)

            qq_M = Message(add, text='QQ号')
            qq = Entry(add)
            user_M = Message(add, text='用户名')
            user = Entry(add)
            qq_M.grid(row=6, column=0)
            qq.grid(row=6, column=1)
            user_M.grid(row=7, column=0)
            user.grid(row=7, column=1)

            addB = Button(add, text='确定', command=lambda: adding(
                {'name': name.get(), 'sex': sex.get(), 'student_number': stu.get(), 'group_number': gro.get(),
                 'qq_number': qq.get(), 'user_type': ut.get(), 'password': ps.get(), 'username': user.get()}))
            addB.grid(row=8,column=1)

            

        def adding(get):
            """向服务器发送增加请求，并在收到回复后，进行增加"""
            packet = Packet_add_info()
            packet.setOperator(operator)
            addMember = GUser.GroupMember()

            packet.setAdd_information()addMember)
            if self.communicate(packet):
                con = []
                if get['user_type']=='一般用户':
                    get['user_type']=1
                elif get['user_type']=='组长':
                    get['user_type']=2
                else :get['user_type']=3

                
                for key in get:
                    con.append(get[key])
                tree.insert('', END, values=get)

        for itm in res2:
            tree.insert("", END, values=itm)
        tree.pack(fill=BOTH, expand=True)

        if self.authority > 1:
            delete = Button(M_N.sub_frame, text='删除', command=deljob)
            add = Button(M_N.sub_frame, text='增加', command=addjob)
            delete.pack(side='right')
            add.pack(side='left')
        self.top.mainloop()

    def back(self):
        '''注册时选择返回选项，发生的事件'''
        self.fm1.pack()
        self.fm2.pack_forget()

    def Regist_check(self, name, un, ps):
        """向服务器发送注册请求"""
        GM = GUser.GroupMember()
        GM.setName(name)
        GM.setUsername(un)
        GM.setPassword(ps)
        GM.setUsertype(self.authority)
        operator = Packet_add_info()
        operator.setAdd_information(GM)

        if self.communicate(operator):
            self.view(un, ps)
        else:

            m = messagebox.askokcancel(title='提示', message='注册失败，请重新注册')

    def Change_Authority(self, event, n):
        """注册时用来改变权限"""
        if n == '一般用户':
            self.authority = 1
        elif n == '组长':
            self.authority = 2
        elif n == '教师':
            self.authority = 3

    def communicate(self, packet):
        """通讯函数，负责与服务器进行沟通，
           ip与端口在创建类时进行指定，
           st表示要传输的内容"""

        
        u = GUser.Master()
        u.setUser_name('bamboo')
        u.setPassword('12345**6')
        packet.setOperator(u)
        bp = pickle.dumps(packet)
        data1 = bp

    
        self.tcpCliSock.send(data1)
        data = self.tcpCliSock.recv(1024)
        res = pickle.loads(data)
        result = res.getPasswordSignal()
        

        self.tcpCliSock.close()
        return result


c = client()
c.Log_check()


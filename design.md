
## 模块化设计介绍如下
![模块图 drawio](https://user-images.githubusercontent.com/88447898/168292833-f2181670-0c4f-433e-aba6-d53867d1e022.svg)


### 1 服务器模块
服务器模块的主要起的作用是数据库同客户端的中介，服务器需要做：
- ~使用多线程的方式，同时对多个客户端服务；~
- ~使用多线程的方式，并发式访问数据库，解决的临界区访问问题；~
- 使用多线程的方式，同时服务多个客户端并且并发式访问数据库；
- 统计相应客户端的数据包括但不限于：在线时间、特殊指标（设置按钮，统计按键点击次数）

类说明：
- ~客户端类，包含数据库登录信息~
- 数据库登录信息用字典存储
- 线程——接受client请求类，设计一个线程处理
- 线程——并发访问database类，设计一个线程处理


- [ ] eg:创建游标的实例代码
```
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    db='stu_info',
    charset='utf8',
)
```

- [ ] eg:数据查询操作实例
```
cur = conn.cursor()
SQL = """select * from info;"""
cur.execute(SQL)
data = cur.fetchall()
print(line * 2)
print("{:<12}{:<12}".format("name", "tele_no"))
print(line * 2)
for name, address, tele_no in data:
    print("{:<12}{:<12}".format(name, tele_no))
print(line * 2)
cur.close()
```

- [ ] eg:数据库增加数据实例
```
cur = conn.cursor()
name = input("name: ")
address = input("address: ")
tele_no = input("telephone: ")
SQL = "insert into info values" + "('" + name + "' ,'" + address + "' ,'" + tele_no + "');"
cur.execute(SQL)
conn.commit()
cur.close()
```
### 2 客户端模块
客户端模块主要是GUI页面设计，以及内部数据逻辑的处理，需要做：
- 登录界面设计；
- 不同权限用户主页面的设计（包含权限信息展示）与底层逻辑；

类说明：
- 登录数据包类，包含登录信息；
- 用户类，包含用户信息；
- 数据展示类，多种数据展示的类；

序列化代码实例：
```
>>> stu = Student('Tom', 19, 1)
>>> print(stu)
Student [name: Tom, age: 19, sno: 1]

# 序列化
>>> var_b = pickle.dumps(stu)
>>> var_b
b'\x80\x03c__main__\nStudent\nq\x00)\x81q\x01}q\x02(X\x04\x00\x00\x00nameq\x03X\x03\x00\x00\x00Tomq\x04X\x03\x00\x00\x00ageq\x05K\x13X\x03\x00\x00\x00snoq\x06K\x01ub.'

# 反序列化
>>> var_c = pickle.loads(var_b)
>>> var_c
Student [name: Tom, age: 19, sno: 1]

```

#### 2.1 登录界面
- 界面设计：包含一个下滑式表，用来选择教师、组长或者一般用户，然后是输入用户名和密码的框，最后是登录按钮，参考QQ登录界面，；
- 数据流：客户端根据用户所选所填，将对应的类序列化后通过tcp协议发送给服务器，服务器进行相应信息匹配后，返回登录信号；
- 其它：根据登录信号设计弹窗，登陆失败（及原因）、登陆超时（及原因）、其它；

#### 2.2 用户主页
如果是第一次登陆，需要填写相应的信息，应有一个界面用来填报信息，对于所有用户，都应该展示**身份信息**，**登陆时间戳等杂项**，其余加上：
- 一般用户：展示所属小组信息，展示需要做的任务列表；
- 组长：展示所有组员信息，展示所属小组信息，展示需要做的任务列表；
- 教师：展示所有小组的可展开列表（展开后显示组长的视图）；
- *数据统计界面：展示统计信息*
- *数据维护界面：展示所需修改部分*

### 3 其他模块
- 暂无设计

## 附：设计图&类图
- [ ] 数据库设计
- 规定：Students：用户类型为3，权限最低；TeamLeaders：用户类型2，权限中等；Master：用户类型1，
- ~权限较高；Administrator：用户类型0，至高权限。计划用两章表表示，根据查询/修改获取内容。~


#模块/类图如下
- ![packages](https://user-images.githubusercontent.com/88447898/170612416-bfc65b8e-68e9-4888-8d03-647807b46002.svg)
- ![classes](https://user-images.githubusercontent.com/88447898/170612436-71dc60a5-51e9-4822-b64d-ab9b012f0cf6.svg)


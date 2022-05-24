import pickle
import socket
import threading
import pymysql

import GPacket


class Server:

    def __init__(self):
        self.__conn = None
        self.__dbInfo = None

    def connectDB(self):
        self.__conn = pymysql.connect(
            host=self.__dbInfo['host'],
            user=self.__dbInfo['user'],
            password=self.__dbInfo['password'],
            db=self.__dbInfo['db'],
            charset=self.__dbInfo['charset'],
        )

    def setDBInfo(self, db_info: dict):
        self.__dbInfo = db_info

    def getDBInfo(self) -> dict:
        return self.__dbInfo

    # 打印stu_info数据库全部信息
    def showInfo(self):
        cur = self.__conn.cursor()
        SQL = """select * from stu_info;"""
        cur.execute(SQL)
        data = cur.fetchall()
        print(data)

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = socket.gethostname()
        port = 8888
        ADDR = (hostname, port)

        server_socket.bind(ADDR)
        server_socket.listen()

        while True:
            client_socket, addr = server_socket.accept()
            response_thread = ResponseClient()
            response_thread.set_conn_and_client(self.__conn, client_socket)
            print('Get connection from:', addr)
            response_thread.start()

        # 这是异步的方式实现连接多个客户端
        # while True:
        #     rs, ws, es = select.select(inputs, [], [])
        #     for r in rs:
        #         if r is server_socket:
        #             c, address = server_socket.accept()
        #             # here we get the address of client.
        #             print('Got connection from ', address)
        #             inputs.append(c)
        #         else:
        #             try:
        #                 data = r.recv(1024)
        #                 disconnect = not data
        #             except socket.error:
        #                 disconnect = True
        #
        #             if disconnect:
        #                 print(r.getpeername(), 'disconnect')
        #                 inputs.remove(r)
        #             else:
        #                 print('Receive from:', r.getpeername())
        #                 # 如果服务器没有导入GPacket包，能使用反序列化后的客户端发送的数据吗？
        #                 # 实测可以，甚至可以调用相应的方法
        #                 self.executeRequest(data)
        #                 print('Request done.')
        #


# 线程类，成员有操作类型和操作对象
# 方法有setter，getter以及各种操作的实现
class ResponseClient(threading.Thread):
    def __init__(self):
        super().__init__()
        # self.__source_server = None
        self.__conn = None
        self.__target_client = None
        self.__packet = None

    def setConn(self, conn):
        self.__conn = conn

    def setPacket(self, packet):
        self.__packet = packet

    def setTarget_client(self, client_socket):
        self.__target_client = client_socket

    def set_conn_and_client(self, conn, client_socket):
        self.__conn = conn
        self.__target_client = client_socket

    def getConn(self):
        return self.__conn

    def getPacket(self):
        return self.__packet

    def getClient(self):
        return self.__target_client

    def recordOperate(self, user_operator, user_target, operate_type):
        SQL_rec = """insert into operate_record values ('""" + user_operator \
                  + "'," + "'" + operate_type + "'," \
                  + "'" + user_target + "'," + 'default);'
        cur = self.__conn.cursor()
        cur.execute(SQL_rec)
        self.__conn.commit()
        cur.close()

    def responseLogin(self):
        """回应登录请求"""
        user = self.__packet.getOperator()
        cur = self.__conn.cursor()
        SQL = """select password from stu_info where user_name = '""" + user.getUser_name() + "'"
        cur.execute(SQL)
        password = cur.fetchone()
        if self.__packet.getOperator().getPassword() in password:
            packet_response = GPacket.Packet_response_login()
            packet_response.setPasswordSignal(True)
            bp_response = pickle.dumps(packet_response)
            self.__target_client.send(bp_response)
        else:
            packet_response = GPacket.Packet_response_login()
            packet_response.setPasswordSignal(False)
            bp_response = pickle.dumps(packet_response)
            self.__target_client.send(bp_response)
        self.recordOperate(user.getUser_name(), user.getUser_name(), 'l')
        cur.close()

    def responseDelete(self):
        """回应删除请求"""
        user = self.__packet.getOperator()
        info = self.__packet.getDelete_info()
        cur = self.__conn.cursor()
        SQL_exe = """delete from stu_info where student_number = '""" + info.getStudent_number() + "'"
        cur.execute(SQL_exe)
        self.__conn.commit()
        # 加上操作是否完成的判断工作，加上返回给客户端的数据,目前只会返回成功。
        cur.close()
        packet_response = GPacket.Packet_response_is_successful()
        packet_response.setOperate_result(True)
        bp_response = pickle.dumps(packet_response)
        self.__target_client.send(bp_response)
        self.recordOperate(user.getUser_name(), info.getUser_name(), 'd')

    def responseUpdate(self):
        user = self.__packet.getOperator()
        info = self.__packet.getUpdate_info()
        cur = self.__conn.cursor()
        info_list = [('name', str(info.getName())),
                     ('sex', str(info.getSex())),
                     ('student_number', str(info.getStudent_number())),
                     ('group_number', str(info.getGroup_number())),
                     ('qq_number', str(info.getQQ_number())),
                     ('user_type', str(info.getUser_type())),
                     ('password', str(info.getPassword())),
                     ('user_name', str(info.getUser_name())), ]
        SQL_exe = """update stu_info set """
        for column, data in info_list:
            SQL_exe += (column + " = '" + data + "', ")
        SQL_exe = SQL_exe[:-1] + ';'
        cur.execute(SQL_exe)
        self.__conn.commit()
        cur.close()
        self.recordOperate(user.getUser_name(), info.getUser_name(), 'u')
        # 告知客户端是否操作成功
        packet_response = GPacket.Packet_response_is_successful()
        packet_response.setOperate_result(True)
        bp_response = pickle.dumps(packet_response)
        self.__target_client.send(bp_response)

    def responseAdd(self):
        user = self.__packet.getOperator()
        info = self.__packet.getAdd_info()
        cur = self.__conn.cursor()
        info_list = [str(info.getUser_name()),
                     str(info.getSex()),
                     str(info.getStudent_number()),
                     str(info.getGroup_number()),
                     str(info.getQQ_number()),
                     str(info.getUser_type()),
                     str(info.getPassword()),
                     str(info.getUser_name()),
                     ]
        SQL_exe = """insert into stu_info values ('"""
        for data in info_list:
            SQL_exe += (data + "' , '")
        SQL_exe = SQL_exe[:-3] + ');'
        cur.execute(SQL_exe)
        self.__conn.commit()
        cur.close()
        packet_response = GPacket.Packet_response_is_successful()
        packet_response.setOperate_result(True)
        bp_response = pickle.dumps(packet_response)
        self.__target_client.send(bp_response)
        self.recordOperate(user.getUser_name(), info.getUser_name(), 'a')

    def responseSearch(self):
        user = self.__packet.getOperator()
        cur = self.__conn.cursor()
        packet_response = GPacket.Packet_response_is_successful()
        SQL_exe = """select * from stu_info"""

        if user.getUser_type() == 0:
            SQL_exe += ';'
            cur.execute(SQL_exe)
            data = cur.fetchall()
        elif user.getUser_type() == 1:
            group_number = user.getGroup_number()
            SQL_exe += "where group_number = '" + group_number + "';"
            cur.execute(SQL_exe)
        elif user.getUser_type() == 2:
            student_number = user.getStudent_number()
            SQL_exe += "where student_number = '" + student_number + "';"
            cur.execute(SQL_exe)
        else:
            packet_response.setOperate_result(False)
            bp_response = pickle.dumps(packet_response)
            self.__target_client.send(bp_response)
            exit(0)
        data_packet = GPacket.Packet_response_data()
        data_packet.setData(data)
        bd = pickle.dumps(data)
        self.__target_client.send(bd)
        cur.close()
        packet_response.setOperate_result(False)
        bp_response = pickle.dumps(packet_response)
        self.__target_client.send(bp_response)
        self.recordOperate(user.getUser_name(), user.getUser_name(), 's')

    def run(self):
        while True:
            data = self.__target_client.recv(1024)
            if not data:
                break
            self.__packet = pickle.loads(data)
            operate_type = self.__packet.getOperate_type()
            if operate_type == 'l':
                self.responseLogin()
            elif operate_type == 'u':
                pass
        print('end...')


if __name__ == '__main__':
    db = {
        'host': 'localhost',
        'user': 'root',
        'password': '1234',
        'db': 'stu_management',
        'charset': 'utf8',
    }

    server = Server()
    server.setDBInfo(db)
    server.connectDB()
    server.run()

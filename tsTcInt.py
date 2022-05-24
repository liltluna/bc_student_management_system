from socket import *
import GPacket
import pickle
import GUser

HOST = 'B-Altair' # 使用的时候修改成服务器对应的名称
PORT = 8888
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

p = GPacket.Packet_login()
u = GUser.Master()
u.setUser_name('bamboo')
u.setPassword('123456')
p.setOperator(u)
bp = pickle.dumps(p)
data1 = bp
while True:
	sig = input('>')
	tcpCliSock.send(data1)
	data = tcpCliSock.recv(BUFSIZ)
	res = pickle.loads(data)
	print(res.getPasswordSignal())
	if not sig:
		break
# 这个鬼东西隐式结束了客户端进程
	

# tcpCliSock.close()
from socket import *
import keyboard
from time import sleep

HOST = '192.168.10.1'
PORT = 8889
BUFSIZ = 1024
ADDRESS = (HOST, PORT)

print('Tello 电脑控制端测试版\n\nAuthor: agoudbg    Based on: Tello SDK\n\n'
      '正在尝试与Tello建立连接...\n\n'
      '*Tello每次开机后仅能与第一个连接的客户端通信。\n'
      ' 请勿重复开启应用，否则将干扰其它客户端的通信。\n\n')

udpClientSocket = socket(AF_INET, SOCK_DGRAM)

# 发送连接命令
udpClientSocket.sendto("command".encode('utf-8'), ADDRESS)
# 接收命令
data, ADDR = udpClientSocket.recvfrom(BUFSIZ)
# 其实如果连接不正常，无法从Tello读取返回值，下面的步骤不会继续
if data.decode('utf-8')=='ok':
    print('连接成功，', end='')
udpClientSocket.sendto("battery?".encode('utf-8'), ADDRESS)
data, ADDR = udpClientSocket.recvfrom(BUFSIZ)
print("剩余电量百分之", end='')
print(data.decode('utf-8'),end='')
print('可以进行后续操作')

SPEED=35

# 摇杆变量设置
lr=0 # 左右
ba=0 # 前后
ud=0 # 上下
ro=0 # 自转

timer=0
def reset():
    global lr,ba,ud,ro
    lr=0
    ba=0
    ud=0
    ro=0
    
# 左右设置
def setlr(x):
    global lr
    if x==1:
        lr=1
    if x==-1:
        lr=-1

# 前后设置
def setba(x):
    global ba
    if x==1:
        ba=1
    if x==-1:
        ba=-1
        
# 上下设置
def setud(x):
    global ud
    if x==1:
        ud=1
    if x==-1:
        ud=-1

# 自转设置
def setro(x):
    global ro
    if x==1:
        ro=1
    if x==-1:
        ro=-1


def abc(x):
    key_a = keyboard.KeyboardEvent('down', 28, 'a')
    key_s = keyboard.KeyboardEvent('down', 28, 's')
    key_d = keyboard.KeyboardEvent('down', 28, 'd')
    key_w = keyboard.KeyboardEvent('down', 28, 'w')
    key_up = keyboard.KeyboardEvent('down', 28, 'up')
    key_down = keyboard.KeyboardEvent('down', 28, 'down')
    key_left = keyboard.KeyboardEvent('down', 28, 'left')
    key_right = keyboard.KeyboardEvent('down', 28, 'right')
    key_t = keyboard.KeyboardEvent('down', 28, 't')
    key_l = keyboard.KeyboardEvent('down', 28, 'l')
    key_e = keyboard.KeyboardEvent('down', 28, 'e')

    
#左右
    if x.event_type == 'down' and x.name == key_a.name:
        setlr(1)
    if x.event_type == 'down' and x.name == key_d.name:
        setlr(-1)
#前后
    if x.event_type == 'down' and x.name == key_w.name:
        setba(1)
    if x.event_type == 'down' and x.name == key_s.name:
        setba(-1)
#上下
    if x.event_type == 'down' and x.name == key_up.name:
        setud(1)
    if x.event_type == 'down' and x.name == key_down.name:
        setud(-1)
#自转
    if x.event_type == 'down' and x.name == key_right.name:
        setro(1)
    if x.event_type == 'down' and x.name == key_left.name:
        setro(-1)
        
             
#按键事件（起飞）
    if x.event_type == 'down' and x.name == key_t.name:
            # 发送数据
        udpClientSocket.sendto('takeoff'.encode('utf-8'), ADDRESS)
            # 接收数据
        data, ADDR = udpClientSocket.recvfrom(BUFSIZ)
        print("服务器端响应：", data.decode('utf-8'))
        
#按键事件（降落）
    if x.event_type == 'down' and x.name == key_l.name:
            # 发送数据
        udpClientSocket.sendto('land'.encode('utf-8'), ADDRESS)
            # 接收数据
        data, ADDR = udpClientSocket.recvfrom(BUFSIZ)
        print("服务器端响应：", data.decode('utf-8'))
        
#按键事件（紧急停浆）
    if x.event_type == 'down' and x.name == key_e.name:
            # 发送数据
        udpClientSocket.sendto('emergency'.encode('utf-8'), ADDRESS)
            # 接收数据
        data, ADDR = udpClientSocket.recvfrom(BUFSIZ)
        print("服务器端响应：", data.decode('utf-8'))
 
while True:
    timer+=1
    if timer==2:
        print('--',lr,ba,ud,ro)
# 这里将执行发送命令
        sendbox ='rc '+str(SPEED*lr)+' '+str(SPEED*ba)+' '+str(SPEED*ud)+' '+str(SPEED*ro)
        print(sendbox)
        # 发送数据
        udpClientSocket.sendto(sendbox.encode('utf-8'), ADDRESS)
        # 接收数据
        #data, ADDR = udpClientSocket.recvfrom(BUFSIZ)
        #print("服务器端响应：", data.decode('utf-8'))# 测试
        # 由于Tello的数据回传没有搞清楚，这里暂时不接收
        reset()
        timer=0
        print('-',lr,ba,ud,ro)
    
    keyboard.hook(abc)
    sleep(0.1)
    

keyboard.wait()

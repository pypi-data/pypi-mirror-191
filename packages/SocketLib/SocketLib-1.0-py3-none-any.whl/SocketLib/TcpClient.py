from socket import *
import socket
import os
import tqdm

def Tcp_Client_Send_Msg(serve_ip, serve_port, send_message):
    tcp_client = socket(AF_INET, SOCK_STREAM)   # 1.创建套接字
    ip = serve_ip           # 2.准备连接服务器，建立连接
    port = int(serve_port)  # 端口要是int类型，所有要转换
    tcp_client.connect((ip, port))  # 连接服务器，建立连接,参数是元组形式
    message = send_message      # 3.准备需要传送的数据
    tcp_client.send(message.encode("gbk"))  # 用的是send方法，不是sendto
    tcp_client.close()      # 4.关闭连接

def Tcp_Client_Recv_Msg(serve_ip, serve_port):
    tcp_client = socket(AF_INET, SOCK_STREAM)   # 1.创建套接字
    ip = serve_ip       # 2.准备连接服务器，建立连接
    port = int(serve_port)  # 端口要是int类型，所有要转换
    tcp_client.connect((ip, port))  # 连接服务器，建立连接,参数是元组形式
    tcp_remsg = tcp_client.recv(1024).decode('utf-8')  # 3.从服务器接收数据,大小根据需求自己设置
    # print(tcp_remsg.decode("gbk"))  # 如果要乱码可以使用tcp_remsg.decode("gbk")
    tcp_client.close()  # 4.关闭连接
    return tcp_remsg

def Tcp_Client_Send_File(serve_ip, serve_port, send_filename):
    SEPARATOR = '<SEPARATOR>'   # 传输数据间隔符
    ip = serve_ip   # 服务器信息
    port = int(serve_port)     # 端口要是int类型，所有要转换
    Buffersize = 4096 * 10     # 文件缓冲区
    filename = send_filename     # 传输文件名字
    file_size = os.path.getsize(filename)   # 文件大小
    tcp_client = socket.socket()     # 创建socket链接
    # print(f'服务器连接中{host}:{port}')
    tcp_client.connect((ip, port))
    # print('与服务器连接成功')
    tcp_client.send(f'{filename}{SEPARATOR}{file_size}'.encode())    # 发送文件名字和文件大小，必须进行编码处理
    progress = tqdm.tqdm(range(file_size), f'发送{filename}', unit='B', unit_divisor=1024)    # 文件传输
    with open(filename, 'rb') as f:
        # 读取文件
        for _ in progress:
            bytes_read = f.read(Buffersize)
            if not bytes_read:
                break
            # sendall 确保网络忙碌的时候，数据仍然可以传输
            tcp_client.sendall(bytes_read)
            progress.update(len(bytes_read))
    tcp_client.close()   # 关闭资源




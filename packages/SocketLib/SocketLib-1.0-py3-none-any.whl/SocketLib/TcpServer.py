import socket
import tqdm
import os

def Tcp_Server_Recv_Msg(serve_ip, serve_port):
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # 1.创建套接字
    ip = serve_ip       # 2.准备连接服务器，建立连接
    port = int(serve_port)  # 端口要是int类型，所有要转换
    tcp_server.bind((ip, port))  # 绑定本机地址和端口
    tcp_server.listen(5)    # 设置监听队列
    connfd, addr = tcp_server.accept()  # 阻塞连接本机的程序
    # print("Connected to", addr)
    tcp_remsg = connfd.recv(1024)    # 设置接收数据的大小
    connfd.close()
    tcp_server.close()
    return tcp_remsg

def Tcp_Server_Send_Msg(serve_ip, serve_port, send_message):
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 1.创建套接字
    ip = serve_ip  # 2.准备连接服务器，建立连接
    port = int(serve_port)  # 端口要是int类型，所有要转换
    tcp_server.bind((ip, port))  # 绑定本机地址和端口
    tcp_server.listen(5)  # 设置监听队列
    connfd, addr = tcp_server.accept()  # 阻塞连接本机的程序
    # print("Connected to", addr)
    message = send_message
    n = connfd.send(message.encode("gbk"))
    connfd.close()
    tcp_server.close()

def Tcp_Server_Recv_File(serve_ip, serve_port):
    ip = serve_ip
    port = serve_port
    SEPARATOR = '<SEPARATOR>'   # 传输数据间隔符
    Buffersize = 4096 * 10  # 文件缓冲区
    tcp_server = socket.socket()
    tcp_server.bind((ip, port))
    tcp_server.listen(128)       # 设置监听数
    # print(f'服务器监听{ip}:{port}')
    client_socket, address = tcp_server.accept()     # 接收客户端连接
    # print(f'客户端{address}连接')    # 打印客户端ip
    received = client_socket.recv(Buffersize).decode()  # 接收客户端信息
    filename, file_size = received.split(SEPARATOR)
    filename = os.path.basename(filename)   # 获取文件的名字,大小
    file_size = int(file_size)
    # 文件接收处理
    progress = tqdm.tqdm(range(file_size), f'接收{filename}', unit='B', unit_divisor=1024, unit_scale=True)
    with open('tcpRecv_' + filename, 'wb') as f:
        for _ in progress:
            # 从客户端读取数据
            bytes_read = client_socket.recv(Buffersize)
            # 如果没有数据传输内容
            if not bytes_read:
                break
            # 读取写入
            f.write(bytes_read)
            # 更新进度条
            progress.update(len(bytes_read))
    # 关闭资源
    client_socket.close()
    tcp_server.close()





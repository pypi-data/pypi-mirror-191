import socket

def Udp_Server_Recv_Msg(serve_ip, serve_port):
    udp_server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    ip = serve_ip
    port = serve_port
    udp_server.bind((ip,port))  #绑定地址（host,port）到套接字
    data,addr = udp_server.recvfrom(1024)  #data是接收到的数据 addr是对方的地址 也就是发送方的地址
    return data.decode('utf-8')

def Udp_Server_Send_Msg(serve_ip, serve_port, message):
    udp_server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    ip = serve_ip
    port = serve_port
    udp_server.bind((ip,port))  #绑定地址（host,port）到套接字
    data,addr = udp_server.recvfrom(1024)  #data是接收到的数据 addr是对方的地址 也就是发送方的地址
    send_data = message
    udp_server.sendto(send_data.encode("gbk"), addr)

def Tcp_Server_Recv_File(serve_ip, serve_port):
    count = 0
    udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = (serve_ip, serve_port)
    udp_server.bind(server_addr)
    while True:
        if count == 0:
            data, client_addr = server_addr.recvfrom(1024)
            # print('connected from %s:%s' % client_addr)
            f = open('udpRecv_'+ data, 'wb')
        data, client_addr = server_addr.recvfrom(1024)
        if str(data) != "b'end'":
            f.write(data)
            # print('recieved ' + str(count) + ' byte')
        else:
            break
        server_addr.sendto('ok'.encode('utf-8'), client_addr)
        count += 1
    # print('recercled' + str(count))
    f.close()
    server_addr.close()




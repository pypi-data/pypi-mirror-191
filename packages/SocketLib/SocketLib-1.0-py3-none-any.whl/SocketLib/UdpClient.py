import socket
import os
import time

def Get_FilePath_FileName_FileExt(filename):
    filepath, tempfilename = os.path.split(filename)
    shotname, extension = os.path.splitext(tempfilename)
    return filepath, shotname, extension


def Udp_Client_Send_Msg(serve_ip, serve_port, send_data):
    udp_client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udp_address = (serve_ip, serve_port)
    udp_client.sendto(send_data.encode('utf-8'), udp_address)
    udp_client.close()

def Udp_Client_Recv_Msg(serve_ip, serve_port):
    udp_client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udp_address = (serve_ip, serve_port)
    udp_client.sendto("send_data".encode('utf-8'), udp_address)
    # udp_client.bind(udp_address)
    reveive_message = udp_client.recv(1024).decode("utf-8")
    udp_client.close()
    return reveive_message

def Udp_Client_Send_File(serve_ip, serve_port, send_filename):
    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    filename = send_filename
    filepath, tempfilename = os.path.split(filename)
    shotname, extension = os.path.splitext(tempfilename)
    udp_address = (serve_ip, serve_port)
    f = open(filename, 'rb')
    count = 0
    flag = 1
    while True:
        if count == 0:
            data = bytes(shotname + extension, encoding="utf8")
            start = time.time()
            udp_client.sendto(data, udp_address)
        data = f.read(1024)
        if str(data) != "b''":
            udp_client.sendto(data, udp_address)
        else:
            udp_client.sendto('end'.encode('utf-8'), udp_address)
            break
        data, server_addr = udp_client.recvfrom(1024)
        count += 1
    udp_client.close


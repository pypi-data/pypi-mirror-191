import requests
import os,socket
import threading

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        #print(ip)
        return ip
    finally:
        s.close()

def send_to(data):
    thread = threading.Thread(name='t1',target= send_to_t,args=(data,))
    thread.start()


def send_get():
    try:
        ip=get_host_ip()
        request = requests.get(url='http://'+ip+'/SArduino_get_data',timeout=1)
        return request.text
    except:
        print('获取失败')

def send_to_t(data):
    try:
        ip=get_host_ip()
        params= {"data":data}
        request = requests.get(url='http://'+ip+'/SArduino_add_data',params=params,timeout=5)
    except:
        print('发送失败')

def send_get_t(data):
    try:
        ip=get_host_ip()
        params= {"data":data}
        request = requests.get(url='http://'+ip+'/SArduino_add_data',params=params,timeout=5)
    except:
        print('发送失败')
import socket
import threading
from queue import Queue

target = '127.0.0.1'
port_range = range(1, 1024)
queue = Queue() 

open_ports = []

def portscan(port, dtype):
    try:
        sock = socket.socket(socket.AF_INET, dtype)
        sock.connect((target, port))
        if port not in open_ports:
            if dtype == socket.SOCK_STREAM:
                open_ports.append((port, 'TCP'))
            elif dtype == socket.SOCK_DGRAM:
                open_ports.append((port, 'UDP'))
        return True
    except:
        return False

def tcp_worker():
    while True:
        port = queue.get()
        if portscan(port, socket.SOCK_STREAM):
            print(f'TCP Port {port} is open!')
        else:
            print(f'TCP Port {port} is closed!')
        queue.task_done()

def udp_worker():
    while True:
        port = queue.get()
        if portscan(port, socket.SOCK_DGRAM):
            print(f'UDP Port {port} is open!')
        else:
            print(f'UDP Port {port} is closed!')
        queue.task_done()
        
for i in range(30):
    t = threading.Thread(target=tcp_worker)
    t.daemon = True
    t.start()

for i in range(30):
    t = threading.Thread(target=udp_worker) 
    t.daemon = True
    t.start()

for port in port_range:
    queue.put(port)
    
queue.join()

with open('open_ports.txt', 'w') as f:
    for port, protocol in open_ports:
        f.write(f'{port}/{protocol}\n')import socket
import threading
from queue import Queue

target = '127.0.0.1'
port_range = range(1, 1024)
queue = Queue() 

open_ports = []

def portscan(port, dtype):
    try:
        sock = socket.socket(socket.AF_INET, dtype)
        sock.connect((target, port))
        if port not in open_ports:
            if dtype == socket.SOCK_STREAM:
                open_ports.append((port, 'TCP'))
            elif dtype == socket.SOCK_DGRAM:
                open_ports.append((port, 'UDP'))
        return True
    except:
        return False

def tcp_worker():
    while True:
        port = queue.get()
        if portscan(port, socket.SOCK_STREAM):
            print(f'TCP Port {port} is open!')
        else:
            print(f'TCP Port {port} is closed!')
        queue.task_done()

def udp_worker():
    while True:
        port = queue.get()
        if portscan(port, socket.SOCK_DGRAM):
            print(f'UDP Port {port} is open!')
        else:
            print(f'UDP Port {port} is closed!')
        queue.task_done()
        
for i in range(30):
    t = threading.Thread(target=tcp_worker)
    t.daemon = True
    t.start()

for i in range(30):
    t = threading.Thread(target=udp_worker) 
    t.daemon = True
    t.start()

for port in port_range:
    queue.put(port)
    
queue.join()

with open('open_ports.txt', 'w') as f:
    for port, protocol in open_ports:
        f.write(f'{port}/{protocol}\n')

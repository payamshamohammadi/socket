from http import client
import socket
import os
import threading
from time import sleep

ip = socket.gethostbyname(socket.gethostname())
port = 4547
ADDR = (ip,port)
buffer = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

print("Server is start...")




def download(connection , filename):
       
          #  Send file in batches with the buffer size
        
    print('Download file... ', filename)

        # progress = tqdm.tqdm(range(
        #     filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    try:
        print('1')
        with open(filename, "rb") as f:
            size = os.fstat(f.fileno()).st_size
            print('2')
            connection.send(str(size).encode())
            print('3')
            c = connection.recv(1024).decode()
            print('4')
            print(c)
            while True:
                data = f.read(1024)
                if not data:
                    break
                connection.sendall(data)
        print("Transfer completed 100%")
    except:
        connection.send(
            "[SERVER] 550 can't access file: Permission denied.".encode())

def upload(connection, filename):

    i = int(connection.recv(1024).decode())
    print(i)
    connection.send('ok'.encode())
    with open(filename, 'wb') as f:
            print('Starting download \n')
            print(filename)
            data = connection.recv(buffer)
            f.write(data)
            le = len(data)
            while le<i:
                data = connection.recv(buffer)
                le +=len(data)
                f.write(data)
            print('done')
            f.close()

def list(connection):
    files = os.listdir('.')
    data = ""
    if len(files)==0:
        data+= "the server is empty"
    else:
        data += "\n".join(f for f in files)
    connection.send(data.encode())

def handel_client(connection,address):
    print(f"Client {address}")
    while True:
        try:
                data = connection.recv(1024).decode().split('\n')
                cmd = data[0]
                if cmd == 'DOWNLOAD':
                        download(connection,data[1])
                elif cmd == 'UPLOAD':
                        upload(connection,data[1])
                elif  cmd == 'LIST':
                        list(connection)
                elif cmd == 'LOGOUT':
                    break
                else:
                    sleep(3)
                    continue
        except:
            sleep(3)
            continue
    connection.close()

                

while True:
    connection, address = server.accept()
    thread = threading.Thread(target = handel_client, kwargs={'connection':connection, 'address':address})
    thread.start()

    

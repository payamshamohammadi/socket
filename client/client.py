
from http import client
import socket
import sys
import os






ip = socket.gethostbyname(socket.gethostname())
port = 4547
ADDR = (ip,port)
buffer = 1024
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)





def download(connection, filename):
        
          #  Download file from a remote server
        
        try:
            connection.send(str("DOWNLOAD\n"+filename).encode())

        except Exception as e:
            print("Couldn't make server request. Make sure a connection has bene established. \nException: {0}".format(str(e)))

        # self.socket.send(filename.encode())

        i = int(connection.recv(1024).decode())
        print(i)
        connection.send('ok'.encode())
        print(i)
        filep = os.path.join("downloads",filename)
        with open(filep, 'wb') as f:
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
         


def upload(connection,filename):

    try:
            connection.send(str("UPLOAD\n"+filename).encode())

    except Exception as e:
            print("Couldn't make server request. Make sure a connection has bene established. \nException: {0}".format(str(e)))


    with open(filename, "rb") as f:
            size = os.fstat(f.fileno()).st_size
            connection.send(str(size).encode())
            c = connection.recv(1024).decode()
            print(c)
            while True:
                data = f.read(1024)
                if not data:
                    break
                connection.sendall(data)
            print("Transfer completed 100%")

def list(connection):
    try:
        connection.send(str("LIST\n"+" ").encode())

    except Exception as e:
            print("Couldn't make server request. Make sure a connection has bene established. \nException: {0}".format(str(e)))
    li = connection.recv(1024).decode()
    li = li.split("\n")
    for i in li:
        print(i)

print("\nFTP Client \n")
while True:

    command = input('Insert a command: ')
    if command.upper() == "DOWNLOAD":
        filename = input('\nInsert filename: ')
        download(client,filename)
    elif command.upper() == "UPLOAD":
        filename = input('\nInsert filename: ')
        upload(client,filename)
    elif command.upper() == "LIST":
        list(client)
    elif command.upper() == "LOGOUT":
        break
client.close()


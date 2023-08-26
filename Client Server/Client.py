import socket
from address import *


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        # sock.listen()
        # sock.sendall('Creating Connection...'.encode('utf-8'))
        while True:
                
            msg = input('Enter Msg: ')
            if msg == '/exit':
                break
            sock.sendall(msg.encode('utf-8'))
            data = sock.recv(55)
            if data.decode('utf-8') != 'False':
                print(data.decode('utf-8'))


if __name__ == '__main__':
    main()

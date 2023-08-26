import socket

host = '127.0.0.1'
port = 5050


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        while True:
            msg = input('Enter Msg: ')
            if msg == '/exit':
                break
            sock.sendall(msg.encode('utf-8'))


if __name__ == '__main__':
    main()

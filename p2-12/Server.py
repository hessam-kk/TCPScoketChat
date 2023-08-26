import socket as s
import threading as th

host = '127.0.0.1'
port = 5050

# function to handle new connection
def new_connection(conn: s.socket, addr):
    try:
        print('[+] New Connection:', addr)
        while True:
            data = conn.recv(32)

            if not data:
                break
            
            if data.decode('utf-8') == '/exit':
                break
            
            print(data.decode('utf-8'))

    except Exception as e:
        print(f'[-] Error: {e}')

    finally:
        conn.close()
        print('[-] Connection Closed:', addr)


def main():
    # Create Socket
    with s.socket(s.AF_INET, s.SOCK_STREAM) as sock:
        # make socket reusable
        sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen()
        # main loop
        while True:
            conn, addr = sock.accept()
            # create new thread for new connection
            t = th.Thread(target=new_connection, args=(conn, addr))
            # start thread
            t.start()

# run main
if __name__ == '__main__':
    main()

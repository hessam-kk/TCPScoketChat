import socket as s
import threading as th
from address import *
from string import digits


def get_time():
    from time import ctime
    print('[+] Time:', ctime())


def fetch_math(s):
    parts = s.split()

    if len(parts) != 3:
        return False

    if any(parts[1] not in '+-*/' for part in parts):
        return False

    if any(part not in digits for part in parts[0]):
        return False

    if any(part not in digits for part in parts[2]):
        return False

    return eval(parts[0] + parts[1] + parts[2])


# function to handle new connection
def new_connection(conn: s.socket, addr):
    try:
        print('[+] New Connection:', addr)
        while True:
            data = conn.recv(32)

            if data:
                if data.decode('utf-8') == '/exit':
                    break

                # return TIME to client
                elif data.decode('utf-8') == '/time':
                    from time import ctime
                    conn.send(b'[+] Time: ' + bytes(ctime(), 'utf-8'))
                    print(f'{addr}: --> ', end='')
                    print(ctime())

                elif data.decode('utf-8')[0] in digits:
                    ans = fetch_math(data.decode('utf-8'))
                    if ans:
                        conn.sendall(bytes(str(ans), 'utf-8'))
                        print(f'{addr}: --> ', end='')
                        print(ans)
                    else:
                        print('[-] Invalid Input:', data.decode('utf-8'))
                        conn.send('[-] Invalid Input'.encode('utf-8'))
                
                else:
                    print(f'{addr}: --> ', end='')
                    print('[-] Invalid Input:', data.decode('utf-8'))
                    conn.send('[-] Invalid Input'.encode('utf-8'))

            # this else is need because if the connection is closed by the client,
            # using ctrl + c, the server will continuelsy receive data from the client
            # and print blank lines
            else:
                break

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
            # please note that t.join() should not be called here,
            # beacuse it will block the main thread until the thread is done
            # which is basically avoid multiple threads running at the same time
            # in other words, the main thread will not be able to receive new connections
            # until the thread is done (closed the connection)


# run main
if __name__ == '__main__':
    main()

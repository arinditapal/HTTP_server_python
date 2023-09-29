import socket


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    conn, addr = server_socket.accept()

    print(conn, addr) 
    with conn:
        data = conn.recv(1024)
        conn.send(b'HTTP/1.1 200 OK\r\n\r\n')

    print("connection ended")

if __name__ == "__main__":
    main()

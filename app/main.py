import socket


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    # print(conn, addr) 
    while True:

        conn, addr = server_socket.accept()
        data = conn.recv(1024).decode('utf-8')
        with conn:
            request_first_line = data.split('\r\n')[0]
            request_path = request_first_line.split()[1]

            print("this is the requrest path:", request_path)

            if request_path == '/':
                print("send the root")
                conn.send(b'HTTP/1.1 200 OK\r\n\r\n')

            elif "/echo/" in request_path:
                print("req has mess")

                message = request_path[6:]
                print(message)

                res_body = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(message)}\r\n\r\n{message}"

                print(message)
                conn.send(res_body.encode('utf-8'))
            else:
                conn.send(b'HTTP/1.1 404 NOT FOUND\r\n\r\n')

        print("connection done")

if __name__ == "__main__":
    main()

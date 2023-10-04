import socket
import time
import threading
import os
import sys

# print(os.getcwd())
# files = os.listdir()

# print(sys.argv)

def handle_conn(conn, thread_no):
        # print("\ninside of a thread: ", thread_no)
        # print("connection: ", conn)
        data = conn.recv(1024).decode('utf-8')

        parsed_data = data.strip().split("\r\n")
        status_line = parsed_data[0]
        parsed_header = parsed_data[1:]

        request_method = status_line.split()[0]
        request_path = status_line.split()[1]

        # print(request_method, request_path)
        # print(parsed_header)
        headers = {}
        for line in parsed_header:
            line = line.split(':')
            headers[line[0].lower()] = line[1].strip()

        # print(f"start line: {status_line} \nheaders: {headers}")


        with conn:

            if request_path == '/':
                # print("send the root")
                conn.send(b'HTTP/1.1 200 OK\r\n\r\n')

            elif request_path == "/sleep":
                time.sleep(30)
                response_body = "HTTP/1.1 200 OK\r\n\r\n"

                conn.send(response_body.encode('utf-8'))

            elif "/user-agent" in request_path:
                response_body = headers['user-agent']
                print("response body: ", response_body)
                response = f"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\ncontent-length: {len(response_body)}\r\n\r\n{response_body}"

                conn.send(response.encode('utf-8'))

            elif "/echo" in request_path:
                print("req has mess")

                message = request_path[6:]
                print(message)

                res_body = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(message)}\r\n\r\n{message}"

                print(message)
                conn.send(res_body.encode('utf-8'))

            elif "/files" in request_path:
                root = os.getcwd()
                new_directory = os.getcwd() + '/' + sys.argv[2]
                os.chdir(new_directory)

                files = os.listdir()
                search_file = request_path[7:]
                print("search file ", search_file, files)

                if search_file.strip() in files:
                    print("true")
                    # # read file
                    body = ''
                    with open(search_file, 'r') as file:
                        body = file.read()
                    body = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length:{len(body)}\r\n\r\n{body}"
                    conn.send(body.encode('utf-8'))
                else:
                    print("false")
                    conn.send(b'HTTP/1.1 404 NOT FOUND\r\n\r\n')
                os.chdir(root)

            else:
                conn.send(b'HTTP/1.1 404 NOT FOUND\r\n\r\n')

        print("connection done\n")

def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    i = 0
    while True:

        conn, addr = server_socket.accept()
        # print("conn: ", conn)
        th = threading.Thread(target=handle_conn, args=(conn, i))
        th.start()
        # print("connection no: ", i)
        i += 1


if __name__ == "__main__":
    main()

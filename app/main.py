import socket
import time
import threading
import os
import sys

# getting the arguments while runing the code
# print(sys.argv)

def handle_conn(conn, thread_no):
        data = conn.recv(1024).decode('utf-8')

        parsed_data = data.strip().split("\r\n")
        status_line = parsed_data[0]
        parsed_header = parsed_data[1:]
        request_body_content = parsed_data[-1]

        print("body of request: ", request_body_content, type(request_body_content))

        request_method = status_line.split()[0]
        request_path = status_line.split()[1]

        headers = {}
        for line in parsed_header:
            line = line.split(': ')
            headers[line[0].lower()] = line[-1].strip()
        
        print(headers)

        with conn:

            if request_path == '/':
                response = "HTTP/1.1 200 OK\r\n\r\n"
                conn.send(response.encode('utf-8'))

            elif request_path == "/sleep":
                time.sleep(30)
                response = "HTTP/1.1 200 OK\r\n\r\n"

                conn.send(response.encode('utf-8'))

            elif "/user-agent" in request_path:
                response = headers['user-agent']
                print("response body: ", response)
                response = f"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\ncontent-length: {len(response)}\r\n\r\n{response}"

                conn.send(response.encode('utf-8'))

            elif "/echo/" in request_path:
                print("req has mess")

                request_message = request_path[6:]
                print(request_message)

                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(request_message)}\r\n\r\n{request_message}"

                print(request_message)
                conn.send(response.encode('utf-8'))

            elif "/files/" in request_path and  request_method == "GET":
                file_name = request_path[7:]
                folder_name = sys.argv[2]
                file_path = os.path.join(folder_name, file_name)
                print("file_path: ", file_path)
                body_of_file = ''

                try:
                    with open(file_path, 'r') as file:
                        body_of_file = file.read()
                    
                    print("contents: ", body_of_file)
                    
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length:{len(body_of_file)}\r\n\r\n{body_of_file}"
                    print(f"\n{response}")

                    conn.send(response.encode('utf-8'))
                except:
                    print("file not found")
                    conn.send(b'HTTP/1.1 404 NOT FOUND\r\n\r\n')

            elif "/files/" in request_path and request_method == "POST":
                file_name = request_path[7:]
                folder_name = sys.argv[2]
                file_path = os.path.join(folder_name, file_name)
                print("file_path: ", file_path)

                with open(file_path, 'w') as file:
                    file.write(request_body_content)

                response = f"HTTP/1.1 201 OK\r\n\r\n"

                conn.send(response.encode('utf-8'))

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

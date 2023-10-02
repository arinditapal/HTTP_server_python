import socket


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    # print(conn, addr) 
    while True:

        conn, addr = server_socket.accept()
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

        print(f"start line: {status_line} \nheaders: {headers}")


        with conn:

            if request_path == '/':
                print("send the root")
                conn.send(b'HTTP/1.1 200 OK\r\n\r\n')

            elif "/user-agent" in request_path:
                response_body = headers['user-agent']
                print("response body: ", response_body)
                response = f"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\ncontent-length: {len(response_body)}\r\n\r\n{response_body}"

                conn.send(response.encode('utf-8'))

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

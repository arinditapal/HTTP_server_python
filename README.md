# HTTP server in python

This is a starting point for Python solutions to the
["Build Your Own HTTP server" Challenge](https://app.codecrafters.io/courses/http-server/overview).

[HTTP](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol) is the
protocol that powers the web. In this challenge, you'll build a HTTP/1.1 server
that is capable of serving multiple clients.


## Required libraries
Install following libraries and import them.
1. socket
2. threading
3. os
4. sys

## Install library
Use pip to install the above, replace socket with the library name you want to install.

```
pip install socket
```

## Bind to port
The first thing in setting HTTP server is binding you server program with a port number, here we bind with port 4221.

```
server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
conn, addr = server_socket.accept()

```

When we accept a client's request using accept() method, we get back some information about the address of the client( IP address of client ) and a connection which we use to send or receive data from the client.

## Response in http
We send response to a request in http in the following format.

```
HTTP/1.1 200 OK
header
body

```

## Status line
The first line is called the status line. It contains http version, status code, status message. It contents different fields bases on a type of message, that is response or request message.

## Request in http
The request format looks like below, notice the change in the status line contents.

```
GET /index.html HTTP/1.1
header
body

```

In request, status line has a method which is the first word in the status line, here its "GET". Then after the "GET", e have "/index.html", this is called path. It tells the server what file to send to client.

## Header of http
The http headers are collection of key:value pairs, each such pair gives some information about the message.
It may look like:

```
GET /index.html HTTP/1.1
HOST: localhost:4221
User-Agent: curl/7.64.1

```

#### List of headers
1. HOST: localhost:4221
2. User-Agent: curl/7.64.1

## Body of http
The body comes below the header, and it can be anythin, plain text, some json data.

#### Body may look like this
```
GET / HTTP/1.1
Host: localhost:4221
User-Agent: curl/7.64.1

This is the body

```
Here "This is the body" is the content of the body in the response by server.


## Parsing
This refers to seperating out the values of information in the request or response to understant what is there and then do something accordingly.






from socket import *


def server(server_port=8000):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("", server_port))
    server_socket.listen(5)
    print("\nServer ready")
    while True:
        connection_socket, address = server_socket.accept()
        print("\nA new http request for the server")
        print("\nTcp handshake : relai-client to server.")
        website = connection_socket.recv(2048)
        print("\nReceiving data from relai-client to server.")
        webhost = website.decode("utf-8")
        webport = 80  # port number service www 80/tcp
        server_tcp = socket(AF_INET, SOCK_STREAM)
        try:
            server_tcp.connect((webhost, webport))
        except gaierror:
            raise ValueError("Failed to connect to '%s:%s': %s" % (webhost, webport, str(gaierror)))
        request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % webhost
        server_tcp.send(request.encode("utf-8"))
        page = server_tcp.recv(2048)
        print("\nReply of web request : ", page)
        print("\nSending reply of server to relai-client")
        connection_socket.send(page)
        print("\nClosing socket of relai-client to server")
        connection_socket.close()


if __name__ == "__main__":
    server()

from socket import *


forbidden = ["www.youtube.com"]


def forbid(name):
    """
    verifie si le site web est interdit ou non
    """
    for element in range(len(forbidden)):
        if forbidden[element] == name:
            return True
    return False


def relai(server_ip="127.0.0.1", server_port=8001):
    print("\nRelai ready")
    while True:
        connection_socket, address = relai_server_socket.accept()
        website = connection_socket.recv(2048)
        print("\nRequested website of client : ", website)
        # verif si site non interdits
        pegi_18 = forbid(website.decode("utf-8"))
        print("\nPegi-18 : ", pegi_18)
        if pegi_18:
            print("\nThe site is prohibited, you will be directed to a prohibited window")
            request = "GET / HTTP/1.1 403 Forbidden"
            print("\nSending data")
            connection_socket.send(request.encode("utf-8"))
            print("\nClosing relai-client socket")
            relai()
        # nouvelle requete
        print("\nRequesting to server")
        relai_socket = socket(AF_INET, SOCK_STREAM)
        relai_socket.connect((server_ip, server_port))
        print("\nTcp handshake : relai-client to server")
        relai_socket.send(website)
        print("\nSending data of relai-client to server")
        modified_website = relai_socket.recv(2048)
        print("\nReceiving data from server")
        connection_socket.send(modified_website)
        print("\nSending data of relai-server to client")
        print("\nClosing socket of relai-server from client")
        connection_socket.close()


if __name__ == "__main__":
    relai_port = 8003
    relai_server_socket = socket(AF_INET, SOCK_STREAM)
    relai_server_socket.bind(("", relai_port))
    relai_server_socket.listen()
    relai()

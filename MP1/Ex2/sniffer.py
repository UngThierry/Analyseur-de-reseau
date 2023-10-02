from socket import *
import time

path_db_relai = "./database/relai/"
log_file_client = "log_file_client.txt"
log_file_server = "log_file_server.txt"


def log_client(request, address):
    """
    log requete client
    """
    file_client = open(path_db_relai+log_file_client, "a")
    sentence = "GET / HTTP/1.1 " + \
        str(request) + " by adress : " + str(address) + \
        " and time " + time.ctime() + " \n "
    file_client.write(sentence)
    file_client.close()


def log_server(respond):
    """
    log reponse serveur
    """
    file_server = open(path_db_relai+log_file_server, "a")
    file_server.write(respond)
    file_server.close()


def relai(server_ip="127.0.0.1", server_port=8000):
    print("\nRelai ready")
    while True:
        connection_socket, address = relai_server_socket.accept()
        website = connection_socket.recv(2048)
        print("\nRequested website of client : ", website)
        # log requete client
        log_client(website.decode("utf-8"), address)
        # nouvelle requete
        print("\nRequesting to server")
        relai_socket = socket(AF_INET, SOCK_STREAM)
        relai_socket.connect((server_ip, server_port))
        print("\nTcp handshake : relai-client to server")
        relai_socket.send(website)
        print("\nSending data of relai-client to server")
        modified_website = relai_socket.recv(2048)
        print("\nReceiving data from server")
        # mise a jour du log server
        log_server(modified_website.decode("utf-8"))
        connection_socket.send(modified_website)
        print("\nSending data of relai-server to client")
        print("\nClosing socket of relai-server from client")
        connection_socket.close()


if __name__ == "__main__":
    relai_port = 8001
    relai_server_socket = socket(AF_INET, SOCK_STREAM)
    relai_server_socket.bind(("", relai_port))
    relai_server_socket.listen()
    relai()

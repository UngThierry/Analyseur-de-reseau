from socket import *
from threading import *
import utils


def handle_client(socket_server, socket_client):
    message_client = utils.receive_message(socket_client)
    while message_client.decode("utf-8") != "exit":
        utils.send_message(socket_server, message_client)
        message_server = utils.receive_message(socket_server)
        utils.send_message(socket_client, message_server)
        message_client = utils.receive_message(socket_client)
    socket_client.close()


def relai(server_ip="127.0.0.1", server_port=1235, relai_port=1234):
    relai_client_socket = socket(AF_INET, SOCK_STREAM)
    relai_client_socket.connect((server_ip, server_port))
    relai_server_socket = socket(AF_INET, SOCK_STREAM)
    relai_server_socket.bind(("", relai_port))
    relai_server_socket.listen(5)
    print("\nRelai ready")
    while True:
        connection_socket, address = relai_server_socket.accept()
        Thread(target=handle_client, args=(
            relai_client_socket, connection_socket, )).start()


if __name__ == "__main__":
    relai()

from socket import *
import utils


def server(server_port=1235):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("", server_port))
    server_socket.listen(5)
    print("\nServer ready")
    connection_socket, address = server_socket.accept()
    while True:
        message = utils.receive_message(connection_socket)
        response = message.decode("utf-8").upper().encode("utf-8")
        print(response)
        utils.send_message(connection_socket, response)


if __name__ == "__main__":
    server()

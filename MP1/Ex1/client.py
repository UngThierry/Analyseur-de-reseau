from socket import *
import utils


def client(server_ip="127.0.0.1", server_port=1234):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print("\nClient ready")
    print("\nType 'exit' to exit")
    message = input("\nInput lowercase sentence : ")
    while message != "exit":
        utils.send_message(client_socket, message.encode("utf-8"))
        response = utils.receive_message(client_socket).decode("utf-8")
        print("\n", response)
        message = input("\nInput lowercase sentence : ")
    utils.send_message(client_socket, message.encode("utf-8"))
    client_socket.close()


if __name__ == "__main__":
    client()

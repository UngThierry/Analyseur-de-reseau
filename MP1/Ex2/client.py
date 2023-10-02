from socket import *


def client(server_ip="127.0.0.1", server_port=8002):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print("\nClient ready")
    print("\nType a website url following the example's form")
    website = input("\nWebsite (Ex : www.google.fr; www.youtube.com) : ")
    print("\nThe website is : ", website)
    client_socket.send(website.encode("utf-8"))
    print("\nSending website to relai-server")
    modified_website = client_socket.recv(2048)
    print("\nWebsite received from relai-server\n")
    print(modified_website.decode("utf-8"))
    client_socket.close()


if __name__ == "__main__":
    client()

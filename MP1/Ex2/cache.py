from socket import *


historique = []


def create_cache(name, message):
    """
    creation d'un fichier qui contient la cache du site web
    """
    file_cache = open(name, "a")
    file_cache.write(message.decode("utf-8"))
    file_cache.close()


def in_cache(name):
    """
    recuperation info du site sur le cache correspondant
    """
    file_cache = open(name, "r")
    print("\nCached data recovery")
    data = file_cache.read()
    file_cache.close()
    return data


def search_file(filename):
    """
    cherche si un fichier existe 
    """
    try:
        with open(filename, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return b''


def relai(server_ip="127.0.0.1", server_port=8001):
    print("\nRelai ready")
    while True:
        print("\nCache : ", historique)
        connection_socket, address = relai_server_socket.accept()
        website = connection_socket.recv(2048)
        print("\nRequested website of client : ", website)
        print("\nCache value : ", historique)
        if search_file(website):
            """
            Verification si site connu du cache si oui,
            on cherche la requete depuis le fichier cache
            """
            print("\nReading cache")
            data = in_cache(website)
            print("\nSending data from the cache")
            connection_socket.send(data.encode("utf-8"))
            print("\nClosing client socket")
            relai()
        else:
            """
            sinon on store l'info puis on fait une requete au serveur
            """
            historique.append(website)
            print("\nStoring information about the request")
            print("\nCache statue : ", historique)
        # nouvelle requete
        print("\nRequesting to server")
        relai_socket = socket(AF_INET, SOCK_STREAM)
        relai_socket.connect((server_ip, server_port))
        print("\nTcp handshake : relai-client to server")
        relai_socket.send(website)
        print("\nSending data of relai-client to server")
        modified_website = relai_socket.recv(2048)
        print("\nReceiving data from server")
        # mise a jour du cache
        create_cache(website, modified_website)
        connection_socket.send(modified_website)
        print("\nSending data of relai-server to client")
        print("\nClosing socket of relai-server from client")
        connection_socket.close()


if __name__ == "__main__":
    relai_port = 8002
    relai_server_socket = socket(AF_INET, SOCK_STREAM)
    relai_server_socket.bind(("", relai_port))
    relai_server_socket.listen()
    relai()

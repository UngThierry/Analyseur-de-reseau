from socket import *
import time


path_db_relai = "./database/relai/"
historique = []
forbidden = ["www.youtube.com"]
log_file_client = "log_file_client.txt"
log_file_server = "log_file_server.txt"


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


def forbid(name):
    """
    verifie si le site web est interdit ou non
    """
    for element in range(len(forbidden)):
        if forbidden[element] == name:
            return True
    return False


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
        print("\nCache : ", historique)
        connection_socket, address = relai_server_socket.accept()
        website = connection_socket.recv(2048)
        print("\nRequested website of client : ", website)
        # log requete client
        log_client(website.decode("utf-8"), address)
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
        # mise a jour du log server
        log_server(modified_website.decode("utf-8"))
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

from exchange import *

class Server(Thread):
    """Class defining the server"""

    def __init__(self, port):
        Thread.__init__(self)
        if not isinstance(port, int):
            print("Port is not an integer")
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind(('', self.__port))
        self.__continuer = True

    @property
    def portserveur(self):
        return self.__port

    @property
    def socketserveur(self):
        return self.__sock

    def run(self):
        self.__sock.listen(5)
        print("Waiting for a connection")
        while self.__continuer:
            try:
                connexion, client = self.__sock.accept()
                ExchangeThread(connexion).start()  # Starts the exchange thread between a new client and the server
            except OSError:
                pass
            except IOError as e:
                print(e)

        print("Server stops running")

    def __stopListening(self):
        self.__continuer = False
        if self.__sock:
            self.__sock.close()


server = Server(8080)
server.start()

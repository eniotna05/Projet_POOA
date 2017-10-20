import socket
from threading import Thread
from exchange import *
import queue


class Server(Thread):
    """Class defining the server"""

    def __init__(self):
        Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind(('',12800))
        self.continuer = True

    def run(self):
        self.sock.listen(5)
        print("Waiting for a connection")
        while self.continuer:
            try:
                connexion,client = self.sock.accept()
                ExchangeThread(connexion).start() #Starts the exchange thread between a new client and the server
            except OSError:
                pass
            except IOError as e:
                print(e)

        print("Server stops running")

    def __stopListening(self):
        self.continuer = False
        if self.sock:
            self.sock.close()

Serveurtest = Server()
Serveurtest.start()
from threading import Thread
import socket
import queue
import struct


connexions = {}#list of the clients connected to the server
identifiant = 0

class ExchangeThread(Thread):
    """Class defining the exchange process on the server side"""
    def __init__(self,sock):
        Thread.__init__(self)
        if not isinstance(sock, socket.socket) or sock is None:
            raise TypeError("Necessite une vraie socket")
        self.sock = sock
        self.reception = []
        global connexions
        connexions[self.sock]=[]
        global identifiant
        self.identifiant = identifiant + 1
        identifiant = identifiant+1
        self.continuer = True
        self.nomUtilisateur = ""

    def __getcommand(self):
        data = bytes()
        while len(data)<1:
            data += self.sock.recv(1 - len(data))
        return data.decode()

    def __getfloat(self):
        data = bytes()
        while len(data)<8:
            data += self.sock.recv(8 - len(data))
        return data.decode()

    def __getmessage(self):
        data = bytes()
        data += self.sock.recv(1024)
        connexions[self.sock].append(data)
        return data.decode()

    def __stopListening(self):
        self.continuer = False
        print("End of communication with client {}".format(self.identifiant))
        self.__sendmessage("The client {} has deconnected".format(self.identifiant))
        if self.sock:
            self.sock.close()

    def __sendmessage(self,message):
        message = message.encode()
        for client in connexions:
            if client != self.sock:
                client.send(message)

    def __stockData(self,data):
        connexions[self.sock].append(data)

    def run(self):
        print("The client {} has just connected".format(self.identifiant))
        self.sock.send("H".encode())
        commande = self.sock.recv(1024)
        commande = commande.decode()

        if commande != "H":
            print("End of communication")

        self.sock.send(b"Veuillez entrer un nom d'utilisateur:")
        self.nomUtilisateur = self.sock.recv(1024)
        message = "Merci " + self.nomUtilisateur.decode()
        print("ok")
        self.sock.send(message.encode())

        while self.continuer:
            if commande == "Q":
                self.__stopListening()
                break
            else:
                commande = self.__getmessage()
                if commande == "R":
                    dim = self.__getmessage()
                    self.__stockData(dim)
                    self.__sendmessage(dim)
                self.__sendmessage(commande)
                for index,elements in enumerate(connexions[self.sock]):
                    print(index,elements)


        self.sock.close()
        print("socket closed")

from threading import Thread
import socket
from stockage_serveur import *

connexions = {}  # Keys: sockets of the clients ; Values: message received from the clients
identifier = 0

class ExchangeThread(Thread):
    """Class defining the exchange process on the server side"""
    def __init__(self,sock):
        Thread.__init__(self)
        if not isinstance(sock, socket.socket) or sock is None:
            raise TypeError("Needs a real socket")
        self.sock = sock
        global identifier
        self.identifier = identifier + 1
        identifier = identifier + 1
        self.continuer = True
        self.username = ""
        self.reception = Stock(self.username)
        global connexions
        connexions[self.sock] = self.reception

    def getTableau(self):
        string = ""
        for socket in connexions:
            string += connexions[socket].convertStockIntoStr() + ","
        string = string[:-2]
        return string.encode()

    def getmessage(self):
        data = bytes()
        data += self.sock.recv(1024)
        return data.decode()

    def sendmessage(self, message, allUsers=False):
        # If allUsers is True, a message is sent to all the client.
        # If allUsers is False, the message is sent to everyone except the client associated to the exchange thread
        message = message.encode()
        if allUsers == True:
            for client in connexions:
                    client.send(message)
        else:
            for client in connexions:
                if client != self.sock:
                    client.send(message)

    def stockData(self, data):
        print(data)
        self.reception.newObject(data)
        for element in self.reception:
            print(self.reception[element])
        return self.reception

    def analyzeCommand(self):
        message = self.getmessage()
        command = message[0]
        if command == "D":
            id = message[1:]
            for socket in connexions:
                try:
                    self.reception.deleteForm(id)
                except KeyError:
                    pass
            self.sendmessage(message)
        elif command == "Q":
            self.stopListening()
        else:
            self.stockData(message)
            self.sendmessage(message)

    def getUserName(self):
        self.sock.send(b"Veuillez entrer un nom d'utilisateur:")
        self.username = self.getmessage()
        message = "Merci " + self.username
        print("Start of the connection with {} ".format(self.username))
        self.sock.send(message.encode())

    def stopListening(self):
        self.continuer = False
        print("End of communication with client {}".format(self.username))
        self.sendmessage("The client {} has disconnected".format(self.username))
        if self.sock:
            self.sock.close()

    def run(self):
        self.sock.send("H".encode())
        commande = self.sock.recv(1024)
        commande = commande.decode()
        if commande != "H":
            print("End of communication")

        self.getUserName()

        if len(connexions) >= 2:
            self.sock.send(self.getTableau())

        while self.continuer:
            self.analyzeCommand()

        self.sock.close()
        print("socket closed")

from threading import Thread, Event
import socket
from stockage_serveur import Stock

# Keys: sockets of the clients ; Values: message received from the clients
connexions = {}


class ExchangeThread(Thread):
    """Class defining the exchange process on the server side"""

    def __init__(self, sock):
        Thread.__init__(self)
        if not isinstance(sock, socket.socket) or sock is None:
            raise TypeError("Needs a real socket")

        self.sock = sock
        self.__exit_request = Event()
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

        self.username = self.getmessage()
        print("Start of the connection with {} ".format(self.username))
        self.sock.send("O".encode())

    def stopListening(self):
        self.__exit_request.set()
        print("End of communication with client {}".format(self.username))

    def run(self):
        self.sock.send("H".encode())
        commande = self.sock.recv(1024)
        commande = commande.decode()
        if commande != "H":
            print("End of communication")
        self.sock.send("O".encode())

        self.getUserName()

        if len(connexions) >= 2:
            self.sock.send(self.getTableau())

        while not self.__exit_request.is_set():
            self.analyzeCommand()

        self.sock.send("O".encode())
        self.sock.close()
        print("socket closed")

    def quit(self):
        self.__exit_request.set()

from threading import Thread
import socket
import queue
import struct


connexions = {}#list of the clients connected to the server


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

    def __getcommand(self):
        data = bytes()
        while len(data)<3:
            data += self.sock.recv(3 - len(data))
        connexions[self.sock].append(data)
        return data.decode()

    def __getfloat(self):
        data = bytes()
        while len(data)<8:
            data += self.sock.recv(8 - len(data))
            return struct.unpack("d", data)[0]

    def run(self):
        print("The client {} has just connected".format(self.sock))
        self.sock.send("H".encode())
        commande = self.sock.recv(1024)
        commande = commande.decode()

        if commande != "H":
            print("End of communication")

        while True:
            commande = self.__getcommand()
            print(commande)
            if commande == "END":
                print("End of communication with client {}".format(self.sock))
                break
            for index,elements in enumerate(connexions[self.sock]):
                print(index,elements)
            commande=commande.encode()
            for client in connexions:
                if client!=self.sock:
                    client.send(commande)

        self.sock.close()

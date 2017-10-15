from threading import Thread
import socket
import struct
import time

userCmd = ""
class Client:
    """Class defining the client"""

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect(('localhost',12800))
        global userCmd
        self.userCmd = userCmd

    def __getmessage(self):
        """Receives a 3-characters long message"""
        commande = bytes()
        while len(commande)<3:
            commande += self.sock.recv(3-len(commande))

        return commande.decode()

    def ___sendcommand(self,sock, commande, op1, op2):
        """Sends a message containing: the type of drawing and the associated data"""
        paquet = bytes()
        paquet += commande.encode()
        paquet += struct.pack("d", float(op1))
        paquet += struct.pack("d", float(op2))
        self.sock.send(paquet)

    def clientRunning(self):
        messageServeur = self.sock.recv(1024)
        print(messageServeur)
        if messageServeur != b"H":#tests if the server sends HLO
            raise ValueError("Protocol error: H expected")
        messageServeur = messageServeur.decode()

        self.sock.send(u"H".encode())#Sends HLO back

        reception = Reception(self.sock)
        reception.start()
        envoi = Envoi(self.sock)
        envoi.start()
        reception.join()
        envoi.join()
        self.sock.close()

class Envoi(Thread):
    """Thread for sending messages to the server"""
    def __init__(self,sock):
        Thread.__init__(self)
        self.sock = sock
        global userCmd
        self.userCmd = userCmd

    def run(self):
        while True:
            if self.userCmd == "END":
                break
            self.userCmd = input(">")
            self.sock.send(self.userCmd.encode())


class Reception(Thread):
    """Thread for reception of messages from the server"""
    def __init__(self,sock):
        Thread.__init__(self)
        self.sock = sock
        global userCmd
        self.userCmd = userCmd

    def run(self):
        while True:
            if self.userCmd == "END":
                print("Fin communication")
            commande = self.sock.recv(1024)
            print(commande)


client1 = Client()
client1.clientRunning()
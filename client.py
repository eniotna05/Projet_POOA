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
        self.continuer = True

    def clientRunning(self):
        messageServeur = self.sock.recv(1024)
        if messageServeur != b"H":#tests if the server sends HLO
            raise ValueError("Protocol error: H expected")
        self.sock.send(u"H".encode())#Sends HLO back

        while self.continuer:
            if self.userCmd =="END":
                break
            else:
                reception = Reception(self.sock)
                reception.start()
                envoi = Envoi(self.sock)
                envoi.start()
                reception.join()
                envoi.join()
        print("End of the game")

class Envoi(Thread):
    """Thread for sending messages to the server"""
    def __init__(self,sock):
        Thread.__init__(self)
        self.sock = sock
        global userCmd
        self.userCmd = userCmd

    def ___sendcommand(self,commande):
        """Sends a message containing: the type of drawing and the associated data"""
        paquet = bytes()
        paquet += commande.encode()
        self.sock.send(paquet)

    def __senddim(self,commande,op1,op2):
        paquet = bytes()
        op1 = str(op1)
        op2 = str(op2)
        paquet += commande.encode()
        paquet += op1.encode()
        paquet += op2.encode()
        self.sock.send(paquet)

    def run(self):
        while True:
            if self.userCmd == "Q":
                break
            else:
                self.userCmd = input(">")
                self.___sendcommand(self.userCmd)

class Reception(Thread):
    """Thread for reception of messages from the server"""
    def __init__(self,sock):
        Thread.__init__(self)
        self.sock = sock
        global userCmd
        self.userCmd = userCmd
        self.continuer = True

    def __getmessage(self):
        """Receives a 3-characters long message"""
        commande = bytes()
        commande += self.sock.recv(1024)
        print(commande.decode())
        return commande.decode()

    def run(self):
        while self.continuer:
            if self.userCmd == "Q":
                self.sock.close()
                print("Fin communication")
                self.continuer=False
            else:
                self.__getmessage()


client2 = Client()
client2.clientRunning()
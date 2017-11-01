from threading import Thread
import socket
from Command_class import *
from string_to_class import *
from Form_class import *
import time
from string_to_class import string_to_command


userCmd = ""


class Client(Thread):
    """Class defining the client"""
    def __init__(self, sending_queue, receiving_queue):
        Thread.__init__(self)
        global userCmd
        self.userCmd = userCmd
        self.continuer = True
        self.sending_queue = sending_queue
        self.receiving_queue = receiving_queue

    def run(self):

        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect(('localhost',12800))

        messageServeur = self.sock.recv(1024)
        if messageServeur != b"H":#tests if the server sends HLO
            raise ValueError("Protocol error: H expected")
        self.sock.send(u"H".encode())#Sends HLO back

        messageServeur = self.sock.recv(1024)
        messageServeur=messageServeur.decode()
        print(messageServeur)
        nomUtilisateur = input(">")
        self.sock.send(nomUtilisateur.encode())
        messageServeur = self.sock.recv(1024)
        messageServeur=messageServeur.decode()
        print(messageServeur)

        reception = Reception(self.sock, self.receiving_queue)
        reception.start()
        envoi = Envoi(self.sock, self.sending_queue)
        envoi.start()
        reception.join()
        envoi.join()
        print("End of the game")


class Envoi(Thread):
    """Thread for sending messages to the server"""
    def __init__(self, sock, queue):
        Thread.__init__(self)
        self.sock = sock
        self.form_queue = queue
        global userCmd
        self.userCmd = userCmd

    def sendcommand(self, commande):
        """Sends a message containing: the type of drawing and the associated data"""
        paquet = bytes()
        paquet += commande.encode()
        self.sock.send(paquet)

    def run(self):
        while True:
            if self.userCmd == "Q":
                break
            else:
                # try:
                command = self.form_queue.get()
                print("sending command to server", command)
                self.sendcommand(command)


class Reception(Thread):
    """Thread for reception of messages from the server"""
    def __init__(self,sock, queue):
        Thread.__init__(self)
        self.sock = sock
        self.form_queue = queue
        global userCmd
        self.userCmd = userCmd
        self.continuer = True

    def getmessage(self):
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
                message = self.getmessage()
                self.form_queue.put(string_to_command(message))

                if type(string_to_command(message)) == "Create":

                    print("created form", string_to_command(message).created_form)




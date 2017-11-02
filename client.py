from threading import Thread, Event
import socket
from Command_class import *
from string_to_class import *
from Form_class import *
import time
from queue import Empty
from string_to_class import string_to_command

WAITING_QUEUE_TIMEOUT = 0.05

class Client(Thread):
    """Class defining the client"""
    def __init__(self, sending_queue, receiving_queue, session_manager):
        Thread.__init__(self)
        self._exit_request = Event()
        self.sending_queue = sending_queue
        self.receiving_queue = receiving_queue
        self.session_manager = session_manager

    def run(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost',12800))

        messageServeur = self.sock.recv(1024)
        if messageServeur != b"H":#tests if the server sends HLO
            raise ValueError("Protocol error: H expected")
        self.sock.send(u"H".encode())#Sends HLO back

        messageServeur = self.sock.recv(1024)
        messageServeur=messageServeur.decode()
        print(messageServeur)

        while self.session_manager.client_id == None:
            time.sleep(0.1)

        self.sock.send(self.session_manager.client_id.encode())

        messageServeur = self.sock.recv(1024)
        messageServeur=messageServeur.decode()
        print(messageServeur)

        self._reception = Reception(self.sock, self.receiving_queue)
        self._reception.start()
        self._envoi = Envoi(self.sock, self.sending_queue)
        self._envoi.start()
        self._reception.join()
        self._envoi.join()
        print("End of the game")

    def quit(self):
        self._exit_request.set()
        print('Exit request in client set')

        # TODO : refactor code and remove these conditions
        if self._reception:
            self._reception.quit()
        if self._envoi:
            self._envoi.quit()


class Envoi(Thread):

    """Thread for sending messages to the server"""
    def __init__(self, sock, queue):
        Thread.__init__(self)
        self.sock = sock
        self.form_queue = queue
        self._exit_request = Event()

    def sendcommand(self, commande):
        """Sends a message containing: the type of drawing and the associated data"""
        paquet = bytes()
        paquet += commande.encode()
        self.sock.send(paquet)

    def run(self):
        while not self._exit_request.is_set():
            try:
                command = self.form_queue.get(timeout=WAITING_QUEUE_TIMEOUT)
                print("sending command to server", command)
                self.sendcommand(command)
            except Empty :
                # the timeout is here just in case the user wants to exit the app
                pass

    def quit(self):
        """Method which is called when the thread needs to be terminated, for
        instance when a user exits the application"""
        self._exit_request.set()


class Reception(Thread):
    """Thread for reception of messages from the server"""
    def __init__(self,sock, queue):
        Thread.__init__(self)
        self.sock = sock
        self.form_queue = queue
        self._exit_request = Event()

    def getmessage(self):
        """Receives a 3-characters long message"""
        commande = bytes()
        # TODO : This function is blocking, so it prenvents from quitting the app
        # properly. We need to modify that behaviour (server closes connection,
        # non-blocking socket or socket timeout)
        commande += self.sock.recv(1024)
        print(commande.decode())
        return commande.decode()

    def run(self):

        while not self._exit_request.is_set():
            message = self.getmessage()
            self.form_queue.put(string_to_command(message))
            if isinstance(string_to_command(message), Create):
                print("created form", string_to_command(message).created_form)
        self.sock.close()
        print("Fin communication")

    def quit(self):
        self._exit_request.set()
        self.sock.close()


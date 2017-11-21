# This file handles the threads associated to the client.
# Sender is used to send messages to the server.
# Receiver is used to receive messages from the server.

from threading import Thread, Event
from queue import Empty
from socket import socket
from time import sleep
from utils.command_class import Create
from utils.string_to_class import string_to_command


WAITING_QUEUE_TIMEOUT = 0.05
SOCKET_TIMEOUT = 0.5
SERVER_PORT = 12800


class Client(Thread):
    """Class defining the client thread, which establishes a connexion with
    the server and then launches two threads, one to send packets over the
    network, and the other one to receive packets"""

    def __init__(self, sending_queue, receiving_queue, session_manager):
        Thread.__init__(self)
        self.sending_queue = sending_queue
        self.receiving_queue = receiving_queue
        self.session_manager = session_manager
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__receiver = Receiver(self.__sock, self.receiving_queue)
        self.__sender = Sender(self.__sock, self.sending_queue)

    def run(self):
        while self.session_manager.client_id is None or \
                self.session_manager.server_ip is None:
            sleep(0.1)

        self.__sock.settimeout(SOCKET_TIMEOUT)
        self.__sock.connect((self.session_manager.server_ip, SERVER_PORT))

        # Tests if the server sends HLO
        server_msg = self.__sock.recv(1024)
        if server_msg != b"H.":
            raise ValueError("Protocol error: H expected")

        # Sends HLO back & waits for confirmation
        self.__sock.send(u"H.".encode())
        server_msg = self.__sock.recv(1024)
        if server_msg != b"O.":
            raise ValueError("Protocol error: O expected")

        # Sends client_id
        self.__sock.send(self.session_manager.client_id.encode())

        # Tests if server has received client_id
        server_msg = self.__sock.recv(1024)
        if server_msg != b"O.":
            raise ValueError("Protocol error: O expected")
        self.session_manager.is_connected = True

        # Start of the threads to receive and send messages
        self.__receiver.start()
        self.__sender.start()
        self.__receiver.join()
        self.__sender.join()

        # Sends 'Q' to the server when the client wants to leave the app
        self.__sock.send(u"Q.".encode())
        try:
            server_msg = self.__sock.recv(1024)
            if server_msg != b"O.":
                raise ValueError("Protocol error: O expected")
        except socket.timeout:
            pass
        self.__sock.close()
        self.session_manager.is_connected = False

    def quit(self):
        if self.__receiver:
            self.__receiver.quit()
        if self.__sender:
            self.__sender.quit()


class Sender(Thread):
    """Thread for sending messages to the server"""

    def __init__(self, sock, queue):
        Thread.__init__(self)
        self.__sock = sock
        self.form_queue = queue
        self.__exit_request = Event()

    def _send_command(self, command):
        """Sends a message"""
        pack = bytes()
        pack += command.encode()
        self.__sock.send(pack)

    def run(self):
        while not self.__exit_request.is_set():
            try:
                command = self.form_queue.get(timeout=WAITING_QUEUE_TIMEOUT)
                command = command + "."
                self._send_command(command)
                print("sending command to server", command)
            except Empty:
                # the timeout is here just in case the user wants to exit the app
                pass

    def quit(self):
        """Method which is called when the thread needs to be terminated, for
        instance when a user exits the application"""
        self.__exit_request.set()


class Receiver(Thread):
    """Thread for receiving messages from the server"""

    def __init__(self, sock, queue):
        Thread.__init__(self)
        self.__sock = sock
        self.form_queue = queue
        self.__exit_request = Event()

    def _get_message(self):
        """Receives a long message"""
        command = bytes()
        # This function is blocking, so it prevents from quitting the app
        # properly. So we put a timeout on the socket to enable propper quitting
        try:
            command += self.__sock.recv(1024)
        except socket.timeout:
            raise socket.timeout
        return command.decode()

    def run(self):

        while not self.__exit_request.is_set():
            try:
                msg = self._get_message()
                for element in msg.split("."):
                    self.form_queue.put(string_to_command(element))
                    if isinstance(string_to_command(element), Create):
                        print("created form",
                              string_to_command(element).created_form)

            except socket.timeout:
                pass

    def quit(self):
        self.__exit_request.set()

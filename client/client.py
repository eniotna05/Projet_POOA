from threading import Thread, Event
from queue import Empty
import socket
import time

from utils.command_class import Create
from utils.string_to_class import string_to_command

WAITING_QUEUE_TIMEOUT = 0.05
SOCKET_TIMEOUT = 0.5
SERVER_URL = 'localhost'
SERVER_PORT = 12800


class Client(Thread):
    """Class defining the client thread, which establishes a connection with
    the server and then launches two threads, one to send packets over the
    network, and the other one to receive packets"""

    def __init__(self, sending_queue, receiving_queue, session_manager):
        Thread.__init__(self)
        self.sending_queue = sending_queue
        self.receiving_queue = receiving_queue
        self.session_manager = session_manager

    def run(self):

        while self.session_manager.client_id is None:
            time.sleep(0.1)

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._sock.settimeout(SOCKET_TIMEOUT)
        self._sock.connect((SERVER_URL, SERVER_PORT))

        # tests if the server sends HLO
        server_msg = self._sock.recv(1024)
        if server_msg != b"H.":
            raise ValueError("Protocol error: H expected")

        # Sends HLO back & waits for confirmation
        self._sock.send(u"H.".encode())
        server_msg = self._sock.recv(1024)
        if server_msg != b"O.":
            raise ValueError("Protocol error: O expected")

        # Sends client_id
        self._sock.send(self.session_manager.client_id.encode())

        server_msg = self._sock.recv(1024)
        if server_msg != b"O.":
            raise ValueError("Protocol error: O expected")
        self.session_manager.is_connected = True

        self._reception = Reception(self._sock, self.receiving_queue)
        self._reception.start()
        self._envoi = Envoi(self._sock, self.sending_queue)
        self._envoi.start()
        self._reception.join()
        self._envoi.join()

        self._sock.send(u"Q.".encode())
        try:
            server_msg = self._sock.recv(1024)
            if server_msg != b"O.":
                raise ValueError("Protocol error: O expected")
        except socket.timeout:
            pass
        self._sock.close()
        self.session_manager.is_connected = False

    def quit(self):
        # TODO : refactor code and remove these conditions
        if self._reception:
            self._reception.quit()
        if self._envoi:
            self._envoi.quit()


class Envoi(Thread):
    """Thread for sending messages to the server"""

    def __init__(self, sock, queue):
        Thread.__init__(self)
        self._sock = sock
        self.form_queue = queue
        self._exit_request = Event()

    def _send_command(self, command):
        """Sends a message containing: the type of drawing and the associated
        data"""
        paquet = bytes()
        paquet += command.encode()
        self._sock.send(paquet)

    def run(self):
        while not self._exit_request.is_set():
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
        self._exit_request.set()


class Reception(Thread):
    """Thread for reception of messages from the server"""

    def __init__(self, sock, queue):
        Thread.__init__(self)
        self._sock = sock
        self.form_queue = queue
        self._exit_request = Event()

    def _get_message(self):
        """Receives a 3-characters long message"""
        command = bytes()
        # This function is blocking, so it prevents from quitting the app
        # properly. So we put a timeout on the socket to enable propper quitting
        try:
            command += self._sock.recv(1024)
        except socket.timeout:
            raise socket.timeout
        return command.decode()

    def run(self):

        while not self._exit_request.is_set():
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
        self._exit_request.set()

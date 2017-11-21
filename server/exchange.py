# File defining the thread that the server starts with each client when the
# client connects

import socket
from threading import Thread, Event


class ExchangeThread(Thread):
    """Class defining the exchange process on the server side, between the
    server and one client."""

    def __init__(self, sock, server_database):
        Thread.__init__(self)
        if not isinstance(sock, socket.socket) or sock is None:
            raise TypeError("Needs a real socket")

        self.__sock = sock
        self.__exit_request = Event()
        self._username = ""
        self.server_database = server_database
        self.server_database.connexions.append(self.__sock)

    def _get_message(self):
        """Methods that gets a message (max length 1024 bytes) from the socket
        with the client."""
        data = bytes()
        data += self.__sock.recv(1024)
        return data.decode()

    def _send_message(self, message):
        """Handle message dispatching from the server to all the clients"""
        message = message.encode()
        for client in self.server_database.connexions:
            if client != self.__sock:
                client.send(message)

    def _analyze_command(self):
        """Method that analyzes the commands received by the server from the
        client, and calls the corresponding actions"""

        message = self._get_message()
        if message != "":
            first_message = ""
            i = 0
            letter = message[0]
            while letter != ".":
                first_message = first_message + letter
                i += 1
                letter = message[i]
            message = message[i + 1:]
            command = first_message[0]
            if command == "D":
                form_id = first_message[1:]
                print(form_id)
                self.server_database.delete_form(form_id)
                self._send_message(first_message)
            elif command == "Q":
                self.quit()
            elif command == "Z" or command == "N":
                self._send_message(first_message)
            elif command == "R" or command == "S" or command == "P" \
                    or command == "E" or command == "L" or command == "C" \
                    or command == "T":
                self.server_database.create_object(first_message)
                if len(self.server_database.connexions) >= 2:
                    self._send_message(first_message)

    def _get_user_name(self):
        self._username = self._get_message()
        print("Start of the connection with {} {}"
              .format(self._username, self.__sock.getpeername()))
        self.__sock.send("O.".encode())

    def run(self):
        self.__sock.send("H.".encode())
        command = self.__sock.recv(1024)
        command = command.decode()
        if command != "H.":
            print("End of communication")
        self.__sock.send("O.".encode())

        self._get_user_name()

        if len(self.server_database.connexions) >= 2:

            print("Sending history")
            history = self.server_database.convert_database_into_str()
            print(history)
            history = history.encode()
            self.__sock.send(history)

        while not self.__exit_request.is_set():
            self._analyze_command()

        self.__sock.send("O.".encode())
        self.__sock.close()

    def quit(self):
        self.__exit_request.set()
        print("End of communication with client {}".format(self._username))

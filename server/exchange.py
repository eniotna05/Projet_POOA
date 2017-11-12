import socket
from threading import Thread, Event

from server.server_database import ServerDatabase



class ExchangeThread(Thread):
    """Class defining the exchange process on the server side"""

    def __init__(self, sock, server_database):
        Thread.__init__(self)
        if not isinstance(sock, socket.socket) or sock is None:
            raise TypeError("Needs a real socket")

        self.sock = sock
        self.__exit_request = Event()
        self.username = ""
        self.server_database = server_database
        self.server_database.connexions.append(self.sock)


    def _get_message(self):
        data = bytes()
        data += self.sock.recv(1024)
        return data.decode()

    def _send_message(self, message, all_users=False):
        # If all_users is True, a message is sent to all the client.
        # If all_users is False, the message is sent to everyone except the
        # client associated to the exchange thread
        message = message.encode()
        if all_users:
            for client in self.server_database.connexions:
                    client.send(message)
        else:
            for client in self.server_database.connexions:
                if client != self.sock:
                    client.send(message)


    def analyze_command(self):
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
                self._stop_listenning()
            elif command == "Z" or command == "N":
                self._send_message(first_message)
            elif command == "R" or command == "S" or command == "P" \
                  or command == "E" or command == "L" or command == "C" \
                  or command == "T":
                self.server_database.new_object(first_message)
                if len(self.server_database.connexions) >= 2:
                    self._send_message(first_message)
        else:
            pass

    def _get_user_name(self):
        self.username = self._get_message()
        print("Start of the connection with {} ".format(self.username))
        self.sock.send("O".encode())

    def _stop_listenning(self):
        self.__exit_request.set()
        print("End of communication with client {}".format(self.username))

    def run(self):
        self.sock.send("H".encode())
        commande = self.sock.recv(1024)
        commande = commande.decode()
        if commande != "H":
            print("End of communication")
        self.sock.send("O".encode())

        self._get_user_name()

        if len(self.server_database.connexions) >= 2:
            
            print("envoi tableau")
            tableau = self.server_database.convert_database_into_str()
            print(tableau)
            tableau = tableau.encode()
            self.sock.send(tableau)


        #TODO : Envoi des objets un par un mais ne fonctione pas
        """if len(self.server_database.connexions) >= 2:
            print("envoi tableau")
            n = len(self.server_database.form_pile) -1
            while n >= 0:
                form_id = self.server_database.form_pile[n]
                string = self.server_database.stock[form_id].get_string() + "."
                print(string)
                string = string.encode()
                self.sock.send(string)
                n = n - 1"""

        while not self.__exit_request.is_set():
            self.analyze_command()

        self.sock.send("O".encode())
        self.sock.close()
        print("socket closed")

    def quit(self):
        self.__exit_request.set()

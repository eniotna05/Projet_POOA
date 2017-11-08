import socket
from threading import Thread, Event

from server.stockage_serveur import Stock

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

    def _get_tableau(self):
        string = ""
        for sock in connexions:
            try:
                string += connexions[sock].convert_stock_into_str()
            except AttributeError:
                pass
        string = string[:-2]
        print(string)
        return string.encode()

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
            for client in connexions:
                    client.send(message)
        else:
            for client in connexions:
                if client != self.sock:
                    client.send(message)

    def _stock_data(self, data):
        self.reception.new_object(data)
        return self.reception

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
                id = message[1:]
                for sock in connexions:
                    try:
                        self.reception.delete_form(id)
                    except KeyError:
                        pass
                self._send_message(first_message)
            elif command == "Q":
                self._stop_listenning()
            elif command == "Z":
                self._send_message(first_message)
            else:
                self._stock_data(first_message)
                if len(connexions) >= 2:
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

        if len(connexions) >= 2:
            print("envoi tableau")
            self.sock.send(self._get_tableau())

        while not self.__exit_request.is_set():
            self.analyze_command()

        self.sock.send("O".encode())
        self.sock.close()
        print("socket closed")

    def quit(self):
        self.__exit_request.set()

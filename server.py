# File defining the main thread of the server

import socket
from threading import Thread, Event
from server.exchange import ExchangeThread
from server.server_database import ServerDatabase


SOCKET_TIMEOUT = 0.5
SERVER_PORT = 12800


class Server(Thread):
    """Class defining the server thread. This thread listen for incoming
    connections and start a new thread for each client"""

    def __init__(self, port):
        Thread.__init__(self)
        if not isinstance(port, int):
            print("Port is not an integer")
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind(('', self.__port))
        self.__sock.settimeout(SOCKET_TIMEOUT)
        self.__exit_request = Event()
        self.__exchange_thread_list = []
        self.database = ServerDatabase()

    def run(self):
        self.__sock.listen(5)
        print("Waiting for a connection")
        while not self.__exit_request.is_set():
            try:
                connexion, client = self.__sock.accept()
                # Starts the exchange thread between a new client and the server
                new_thread = ExchangeThread(connexion, self.database)
                new_thread.start()
                self.__exchange_thread_list.append(new_thread)
            except OSError:
                pass
            except IOError as e:
                print(e)
            except KeyboardInterrupt:
                self.quit()
            except socket.timeout:
                pass

        print("Server stops running")

    def quit(self):
        print(self.__exchange_thread_list)
        self.__exit_request.set()
        for t in self.__exchange_thread_list:
            t.quit()
        for t in self.__exchange_thread_list:
            t.join()
        if self.__sock:
            self.__sock.close()


if __name__ == '__main__':
    server = Server(SERVER_PORT)
    server.start()
    server.join()

from threading import Thread, Event
import socket
import time
from exchange import ExchangeThread

SOCKET_TIMEOUT = 0.5


class Server(Thread):
    """Class defining the server"""

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

    @property
    def portserveur(self):
        return self.__port

    @property
    def socketserveur(self):
        return self.__sock

    def run(self):
        self.__sock.listen(5)
        print("Waiting for a connection")
        while not self.__exit_request.is_set():
            try:
                connexion, client = self.__sock.accept()
                # Starts the exchange thread between a new client and the server
                new_thread = ExchangeThread(connexion)
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
    server = Server(12800)
    server.start()
    server.join()

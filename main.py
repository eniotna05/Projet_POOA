from kivy.app import App
from kivy.uix.widget import Widget
from queue import Queue

from Widget import WhiteboardInstance, Toolbar
from client import Client


class WhiteboardApp(App):

    def __init__(self):
        super().__init__()
        self.sending_queue = Queue()
        self.client_thread = Client(self.sending_queue)
        self.board = WhiteboardInstance(self.sending_queue)
        self.toolbar = Toolbar(self.board)

    def build(self):
        parent = Widget()
        self.client_thread.start()
        parent.add_widget(self.toolbar)
        parent.add_widget(self.board)

        return parent


if __name__ == '__main__':
    MyApp = WhiteboardApp()
    MyApp.run()

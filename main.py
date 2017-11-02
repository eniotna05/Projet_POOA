# This file handles the main thread of the client application
# Before launching it, make sure that the server is launched with
# "python server.py" command (therfore the client can connect)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color
from kivy.clock import Clock
from queue import Queue

from sessionManager import SessionManager
from whiteboardInstance import WhiteboardInstance
from toolbar import Toolbar
from client import Client
from Command_class import *


class WhiteboardApp(App):

    def __init__(self):
        super().__init__()
        self.sending_queue = Queue()
        self.receiving_queue = Queue()
        self.session_manager = SessionManager(self.sending_queue)
        self.client_thread = Client(self.sending_queue, self.receiving_queue,
                                    self.session_manager)
        self.board = WhiteboardInstance(self.sending_queue, self.session_manager)
        self.toolbar = Toolbar(self.board, self.client_thread, self.session_manager)
        self.toolbar.size_hint = (0.2, 1)
        self.board.size_hint = (0.8, 1)
        # self.toolbar.pos_hint = {'x': self.toolbar.width}
        # self.board.pos_hint = {'x': 0.2}

    def build(self):
        parent = BoxLayout()
        self.client_thread.start()
        # self.toolbar.size_hint = (None, None)
        # self.toolbar.size = (200, 600)
        # self.toolbar.pos = (0, 0)
        # self.board.size_hint = (None, None)
        # self.board.size = (600, 600)
        # self.board.pos = (200, 0)
        # self.toolbar.pos_hint = {}

        # self.board.pos_hint = {'x': 0.2}
        parent.add_widget(self.board)
        parent.add_widget(self.toolbar, 0)

        Clock.schedule_interval(self.execute_command, 1 / 30)

        return parent


    # the main thread needs to be in charge of all the drawing, so we check
    # regularly if the client has received new forms and draw them eventually

    def execute_command(self, dt):

        while not self.receiving_queue.empty():
            new_command = self.receiving_queue.get()



            if isinstance(new_command,Create):
                self.board.draw_form(new_command.created_form)


if __name__ == '__main__':
    MyApp = WhiteboardApp()
    MyApp.run()

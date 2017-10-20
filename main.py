from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from queue import Queue


from Widget import WhiteboardInstance, Toolbar
from client import Client


class WhiteboardApp(App):

    def __init__(self):
        super().__init__()
        self.sending_queue = Queue()
        self.receiving_queue = Queue()
        self.client_thread = Client(self.sending_queue, self.receiving_queue)
        self.board = WhiteboardInstance(self.sending_queue)
        self.toolbar = Toolbar(self.board)

    def build(self):
        parent = Widget()
        self.client_thread.start()
        parent.add_widget(self.toolbar)
        parent.add_widget(self.board)
        Clock.schedule_interval(self.draw_received_forms, 1 / 30)

        return parent

    def draw_received_forms(self, dt):
        while not self.receiving_queue.empty():
            new_form = self.receiving_queue.get()
            self.board.draw_form(new_form)


if __name__ == '__main__':
    MyApp = WhiteboardApp()
    MyApp.run()

# This file handles the main thread of the client application
# Before launching it, make sure that the server is launched with
# "python server.py" command (therfore the client can connect)


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from queue import Queue

from client.popup import Start_Popup
from client.session_manager import SessionManager
from client.whiteboard_instance import WhiteboardInstance
from client.toolbar import Toolbar
from client.client import Client
from utils.command_class import Create, Delete, DeleteRequest, NegativeAnswer


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
        self.start_popup = Start_Popup()

    def build(self):
        parent = BoxLayout()
        self.client_thread.start()

        parent.add_widget(self.board)
        parent.add_widget(self.toolbar, 0)

        Clock.schedule_interval(self.execute_command, 1 / 30)

        return parent

    def on_start(self):
        self.start_popup.open()
        # TODO : à améliorer
        # pas très clean ça, d'accéder à un objet et de bind une de ses propriétés
        # à l'extérieur. Mieux vaut écouter on_dismiss de l'objet Popup et
        # récupérer la valeur stockée dans Popup à ce moment là;-)
        self.start_popup.text_input.bind(on_text_validate=self.update_username)

    def update_username(self, instance):
        self.session_manager.client_id = self.start_popup.text_input.text

    # the main thread needs to be in charge of all the drawing, so we check
    # regularly if the client has received new forms and draw them eventually
    def execute_command(self, dt):
        while not self.receiving_queue.empty():
            new_command = self.receiving_queue.get()

            if isinstance(new_command, Create):
                self.board.draw_form(new_command.created_form)

            if isinstance(new_command, Delete):
                self.board.delete_form_in_canvas(new_command.form_id)

            if isinstance(new_command, DeleteRequest):
                if new_command.form_id.split("-")[0] == \
                        self.session_manager.client_id:
                    response = str(input("""{} wishes to delete one of the form that you created: {},
                                           type o to accept and n to refuse \n
                                           """.format(new_command.requester, new_command.form_id)))
                    if response == "n" or response == "N":
                        self.sending_queue.put(NegativeAnswer(new_command.form_id, new_command.requester).get_string())
                    else:
                        self.board.delete_form_in_canvas(new_command.form_id, send_to_server=True)

            if isinstance(new_command, NegativeAnswer):
                if new_command.receptor == \
                        self.session_manager.client_id:
                    emettor = new_command.form_id.split("-")[0]
                    print("{} does not wish you to delete his form: {}"
                          .format(emettor, new_command.form_id))

    def on_stop(self):
        self.client_thread.quit()
        self.client_thread.join()


if __name__ == '__main__':
    MyApp = WhiteboardApp()
    MyApp.run()

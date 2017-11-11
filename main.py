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
from client.popup2 import *


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
        self.start_popup = Input_Popup("Username",
                                       "Please enter your name",
                                       "John Doe",
                                       Error_Popup("You have not entered your name !"))
        self.question_popup = Question_Popup("", "")
        self.answer = ""
        self.command = ""
        self.requester = ""

    def build(self):
        parent = BoxLayout()
        self.client_thread.start()

        parent.add_widget(self.board)
        parent.add_widget(self.toolbar, 0)

        Clock.schedule_interval(self.execute_command, 1 / 30)

        return parent

    def on_start(self):
        self.start_popup.open()
        self.start_popup.bind(on_dismiss=self.update_username)

    def update_username(self, instance):
        self.session_manager.client_id = instance.return_value


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
                    question = str(new_command.requester) + " wishes to delete \n"\
                               + "one of the form that you created : " + str(new_command.form_id)
                    self.question_popup = Question_Popup("Someone would like to delete one of your shape", question)
                    self.question_popup.bind(on_dismiss=self.update_answer)
                    self.question_popup.open()
                    self.command = new_command.form_id
                    self.requester = new_command.requester
                    #if self.answer != "":
                    #    if self.answer == "no":
                    #        self.sending_queue.put(NegativeAnswer(new_command.form_id,
                    #                                              new_command.requester).get_string())
                    #    else:
                    #        self.board.delete_form_in_canvas(new_command.form_id, send_to_server=True)

            if isinstance(new_command, NegativeAnswer):
                if new_command.receptor == self.session_manager.client_id:
                    emettor = new_command.form_id.split("-")[0]
                    refusal_text = str(emettor) + "does not wish you to delete his form:" \
                           + str(new_command.form_id)
                    refusal_popup = Error_Popup(text_content=refusal_text)
                    refusal_popup.open()


    def update_answer(self, instance):
        if instance.return_value == "no":
            self.sending_queue.put(NegativeAnswer(self.command, self.requester).get_string())
        else:
            self.board.delete_form_in_canvas(self.command, send_to_server=True)


    def on_stop(self):
        self.client_thread.quit()
        self.client_thread.join()


if __name__ == '__main__':
    MyApp = WhiteboardApp()
    MyApp.run()

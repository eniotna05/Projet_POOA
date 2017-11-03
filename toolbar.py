from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from sessionManager import SessionManager

from formTypes import Forms


class Toolbar(BoxLayout):
    """Class defining the buttons of the left-side toolbar"""

    def __init__(self, white_board, client_thread_manager, session_manager):
        super().__init__(orientation='vertical')
        self.white_board = white_board
        self.selected_form = None
        self.client_thread_manager = client_thread_manager
        self.session_manager = session_manager

        self.name_input = TextInput(text='', multiline=False)
        self.name_input.bind(on_text_validate=self.set_name)
        self.add_widget(self.name_input)

        self.print_btn = Button(text="Print St")
        self.print_btn.bind(on_release=self.print_status)
        self.add_widget(self.print_btn)


        self.quit_btn = Button(text="Quit")
        self.quit_btn.bind(on_release=self.quit)
        self.add_widget(self.quit_btn)

        self.delete_last_btn = Button(text="Delete Last")
        self.delete_last_btn.bind(on_release=self.delete_last)
        self.add_widget(self.delete_last_btn)

        self.select_line_btn = Button(text="Line")
        self.select_line_btn.bind(on_release=self.select_line)
        self.add_widget(self.select_line_btn)

        self.select_rect_btn = Button(text="Rectangle")
        self.select_rect_btn.bind(on_release=self.select_rect)
        self.add_widget(self.select_rect_btn)

        self.select_square_btn = Button(text="Square")
        self.select_square_btn.bind(on_release=self.select_square)
        self.add_widget(self.select_square_btn)

        self.select_ellipse_btn = Button(text="Ellipse")
        self.select_ellipse_btn.bind(on_release=self.select_ellipse)
        self.add_widget(self.select_ellipse_btn)

        self.select_circle_btn = Button(text="Circle")
        self.select_circle_btn.bind(on_release=self.select_circle)
        self.add_widget(self.select_circle_btn)

    def set_name(self, value):
        self.session_manager.client_id = value.text

    def quit(self, obj):
        self.client_thread_manager.quit()

    def delete_last(self, obj):
        group_name = str(SessionManager.client_id)\
                     + str(SessionManager.form_number)
        self.white_board.canvas.remove_group(group_name)


    def print_status(self, obj):
        print(self.white_board.canvas.children)



    def select_line(self, obj):
        self.white_board.selected_form = Forms.LINE

    def select_rect(self, obj):
        self.white_board.selected_form = Forms.RECT

    def select_square(self, obj):
        self.white_board.selected_form = Forms.SQUARE

    def select_ellipse(self, obj):
        self.white_board.selected_form = Forms.ELLIPSE

    def select_circle(self, obj):
        self.white_board.selected_form = Forms.CIRCLE



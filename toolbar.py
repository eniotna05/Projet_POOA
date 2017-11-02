from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from formTypes import Forms


class Toolbar(BoxLayout):
    """Class defining the buttons of the left-side toolbar"""

    def __init__(self, white_board, client_thread_manager):
        super().__init__(orientation='vertical')
        self.white_board = white_board
        self.selected_form = None
        self.client_thread_manager = client_thread_manager

        self.print_btn = Button(text="Print St")
        self.print_btn.bind(on_release=self.print_status)
        self.add_widget(self.print_btn)


        self.quit_btn = Button(text="Quit")
        self.quit_btn.bind(on_release=self.quit)
        self.add_widget(self.quit_btn)

        self.delete_btn = Button(text="Delete")
        self.delete_btn.bind(on_release=self.delete_item)
        self.add_widget(self.delete_btn)

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

    def quit(self, obj):
        self.client_thread_manager.quit()

    def delete_item(self, obj):
        self.white_board.canvas.remove_group("1")


        """canvas_objects = self.white_board.canvas.get_group("1")
        print(canvas_objects)
        for k in canvas_objects:
            self.white_board.canvas.remove(k)"""


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


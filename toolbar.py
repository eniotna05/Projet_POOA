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

        self.quit_btn = Button(text="Quit")
        self.quit_btn.bind(on_release=self.quit)
        self.add_widget(self.quit_btn)

        self.clear_btn = Button(text="Clear")
        self.clear_btn.bind(on_release=self.clear_board)
        self.add_widget(self.clear_btn)

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

        self.select_image_btn = Button(text="Image")
        self.select_image_btn.bind(on_release=self.select_image)
        self.add_widget(self.select_image_btn)

    def quit(self, obj):
        self.client_thread_manager.quit()

    def clear_board(self, obj):
        self.white_board.canvas.clear()

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

    def select_image(self, obj):
        self.white_board.selected_form = Forms.IMAGE
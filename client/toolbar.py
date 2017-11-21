from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.colorpicker import ColorPicker

from utils.form_types import Forms

Button_pushed_theme = "atlas://data/images/defaulttheme/button_pressed"
Button_normal_theme = "atlas://data/images/defaulttheme/button"


class Toolbar(BoxLayout):
    """Class defining the buttons of the left-side toolbar"""

    def __init__(self, white_board, client_thread, session_manager):
        super().__init__(orientation='vertical')
        self.white_board = white_board
        self.selected_form = None
        self.client_thread = client_thread
        self.session_manager = session_manager

        Clock.schedule_interval(self.update_network_status, 1 / 30)

        self.connected_label = Label(text="Offline")
        self.add_widget(self.connected_label)

        self.quit_btn = Button(text="Quit")
        self.quit_btn.bind(on_press=self.unpress_all, on_release=self.quit)
        self.add_widget(self.quit_btn)

        self.delete_last_btn = Button(text="Delete Last")
        self.delete_last_btn.bind(on_press=self.unpress_all, on_release=self.delete_last)
        self.add_widget(self.delete_last_btn)

        self.delete_selected_btn = Button(text="Delete Selected")
        self.delete_selected_btn.bind(on_press=self.unpress_all, on_release=self.delete_selected)
        self.add_widget(self.delete_selected_btn)

        self.color_picker = ColorPicker(color=(1, 0, 0, 1), size_hint=(1, 5))
        self.color_picker.bind(color=self.choose_color)
        self.add_widget(self.color_picker)

        self.select_text_btn = Button(text="Write Text")
        self.select_text_btn.bind(on_press=self.unpress_all, on_release=self.select_text)
        self.add_widget(self.select_text_btn)

        self.select_line_btn = Button(text="Line")
        self.select_line_btn.bind(on_press=self.unpress_all, on_release=self.select_line)
        self.add_widget(self.select_line_btn)

        self.select_rect_btn = Button(text="Rectangle")
        self.select_rect_btn.bind(on_press=self.unpress_all, on_release=self.select_rect)
        self.add_widget(self.select_rect_btn)

        self.select_square_btn = Button(text="Square")
        self.select_square_btn.bind(on_press=self.unpress_all, on_release=self.select_square)
        self.add_widget(self.select_square_btn)

        self.select_ellipse_btn = Button(text="Ellipse")
        self.select_ellipse_btn.bind(on_press=self.unpress_all, on_release=self.select_ellipse)
        self.add_widget(self.select_ellipse_btn)

        self.select_circle_btn = Button(text="Circle")
        self.select_circle_btn.bind(on_press=self.unpress_all, on_release=self.select_circle)
        self.add_widget(self.select_circle_btn)

        self.select_image_btn = Button(text="Image")
        self.select_image_btn.bind(on_press=self.unpress_all, on_release=self.select_image)
        self.add_widget(self.select_image_btn)

        self.button_to_unpress_list = [
            self.delete_selected_btn,
            self.select_line_btn,
            self.select_text_btn,
            self.select_rect_btn,
            self.select_square_btn,
            self.select_ellipse_btn,
            self.select_circle_btn,
            self.select_image_btn
        ]

    def unpress_all(self, obj):
        """Change the background_color of the button when another one is
        selected"""
        for button in self.button_to_unpress_list:
            button.background_color = [1, 1, 1, 1]

    def update_network_status(self, dt):
        if self.session_manager.is_connected:
            self.connected_label.text = "Online"
            self.connected_label.color = 0, 1, 0, 1
        else:
            self.connected_label.text = "Offline"
            self.connected_label.color = 1, 0, 0, 1

    def quit(self, obj):
        App.get_running_app().stop()

    def delete_last(self, obj):
        last_form_id = self.session_manager.extract_last_created()
        if last_form_id is not None:
            self.white_board.delete_form_in_canvas(last_form_id, "int")

    def delete_selected(self, obj):
        if self.white_board.selected_form == Forms.DELETE:
            self.white_board.selected_form = None
        else:
            self.white_board.selected_form = Forms.DELETE
            self.delete_selected_btn.background_color = [0, 0, 0, 0]

    def choose_color(self, instance, value):
        self.white_board.drawing_color = value

    def select_text(self, instance):
        if self.white_board.selected_form == Forms.TEXT:
            self.white_board.selected_form = None
        else:
            self.white_board.selected_form = Forms.TEXT
            self.select_text_btn.background_color = [0, 0, 0, 0]

    def select_line(self, obj):
        if self.white_board.selected_form == Forms.LINE:
            self.white_board.selected_form = None
        else:
            self.white_board.selected_form = Forms.LINE
            self.select_line_btn.background_color = [0, 0, 0, 0]

    def select_rect(self, obj):
        if self.white_board.selected_form == Forms.RECT:
            self.white_board.selected_form = None
        else:
            self.white_board.selected_form = Forms.RECT
            self.select_rect_btn.background_color = [0, 0, 0, 0]

    def select_square(self, obj):
        if self.white_board.selected_form == Forms.SQUARE:
            self.white_board.selected_form = None
        else:
            self.white_board.selected_form = Forms.SQUARE
            self.select_square_btn.background_color = [0, 0, 0, 0]

    def select_ellipse(self, obj):
        if self.white_board.selected_form == Forms.ELLIPSE:
            self.white_board.selected_form = None
        else:
            self.white_board.selected_form = Forms.ELLIPSE
            self.select_ellipse_btn.background_color = [0, 0, 0, 0]

    def select_circle(self, obj):
        if self.white_board.selected_form == Forms.CIRCLE:
            self.white_board.selected_form = None
        else:
            self.white_board.selected_form = Forms.CIRCLE
            self.select_circle_btn.background_color = [0, 0, 0, 0]

    def select_image(self, obj):
        if self.white_board.selected_form == Forms.IMAGE:
            self.white_board.selected_form = None
        else:
            self.white_board.selected_form = Forms.IMAGE
            self.select_image_btn.background_color = [0, 0, 0, 0]

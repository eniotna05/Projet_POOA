
from Command_class import *
from Form_class import *
from string_to_class import *


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Line, Ellipse
from kivy.properties import NumericProperty

from enum import Enum

client_form_database = {}
form_number = 0
client_id = "yoann"


class WhiteboardInstance(Widget):

    touch_origin_x = NumericProperty(0)
    touch_origin_y = NumericProperty(0)

    def __init__(self):
        super().__init__()
        self.drawing = False
        self._selected_form = None

    def on_touch_down(self, touch):
        self.drawing = True
        self.touch_origin_x = touch.x
        self.touch_origin_y = touch.y
        print("down", touch.x, touch.y)
        with self.canvas:
            if self._selected_form == Forms.LINE:
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=5)
            elif self._selected_form == Forms.RECT:
                touch.ud['rect'] = Rectangle(pos=(touch.x, touch.y), size=(0, 0))
            elif self._selected_form == Forms.SQUARE:
                touch.ud['square'] = Rectangle(pos=(touch.x, touch.y), size=(0, 0))
            elif self._selected_form == Forms.ELLIPSE:
                touch.ud['ellipse'] = Ellipse(pos=(touch.x, touch.y), size=(0, 0))

    def on_touch_move(self, touch):

        if self._selected_form == Forms.LINE:
            if len(touch.ud['line'].points) <= 2:
                touch.ud['line'].points += (touch.x, touch.y)
                print('second point, line : ', touch.ud['line'].points, 'coords : ', touch.x, touch.y)
            else:
                del touch.ud['line'].points[-2:]
                touch.ud['line'].points += [touch.x, touch.y]
                print('other point, line : ', touch.ud['line'].points,
                      'coords : ', touch.x, touch.y)

        elif self._selected_form == Forms.RECT:
            touch.ud['rect'].size = touch.x - self.touch_origin_x, touch.y - self.touch_origin_y
        elif self._selected_form == Forms.SQUARE:
            dx = touch.x - self.touch_origin_x
            dy = touch.y - self.touch_origin_y
            l = max(abs(dx), abs(dy))
            sign = lambda x: (1, -1)[x < 0]
            touch.ud['square'].size = sign(dx) * l, sign(dy) * l

        elif self._selected_form == Forms.ELLIPSE:
            touch.ud['ellipse'].size = touch.x - self.touch_origin_x, touch.y - self.touch_origin_y

    def on_touch_up(self, touch):
        self.drawing = False
        global client_form_database
        global form_number
        global client_id



        
        if self._selected_form == Forms.LINE:
            del touch.ud['line'].points[-2:]
            print('removing last point, line : ', touch.ud['line'].points)
            touch.ud['line'].points += [touch.x, touch.y]
            print('last point, line : ', touch.ud['line'].points,
                  'coords : ', touch.x, touch.y)
            a = Point(self.touch_origin_x,self.touch_origin_y)
            b = Point(touch.x, touch.y)
            form_number +=1
            client_form_database.append(Lign(a,b,identifier = client_id + form_number))
            self.string_to_send = Lign(a,b,identifier = client_id + form_number).get_string()
        elif self._selected_form == Forms.RECT:
            pass
        elif self._selected_form == Forms.SQUARE:
            pass
        elif self._selected_form == Forms.ELLIPSE:
            pass

    @property
    def selected_form(self):
        return self._selected_form

    @selected_form.setter
    def selected_form(self, selected=None):
        self._selected_form = selected


class Forms(Enum):
    LINE = 1
    RECT = 2
    SQUARE = 3
    ELLIPSE = 4


class Toolbar(BoxLayout):

    def __init__(self, white_board):
        super().__init__(orientation='vertical')
        self.white_board = white_board
        self.selected_form = None

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

    def select_line(self, obj):
        self.white_board.selected_form = Forms.LINE

    def select_rect(self, obj):
        self.white_board.selected_form = Forms.RECT

    def select_square(self, obj):
        self.white_board.selected_form = Forms.SQUARE

    def select_ellipse(self, obj):
        self.white_board.selected_form = Forms.ELLIPSE

    def clear_board(self, obj):
        self.white_board.canvas.clear()


class WhiteboardApp(App):

    def __init__(self):
        super().__init__()
        self.board = WhiteboardInstance()
        self.toolbar = Toolbar(self.board)

    def build(self):
        parent = Widget()
        parent.add_widget(self.toolbar)
        parent.add_widget(self.board)
        return parent


if __name__ == '__main__':
    MyApp = WhiteboardApp()
    MyApp.run()

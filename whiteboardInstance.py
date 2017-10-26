from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle, Line, Ellipse
from kivy.properties import NumericProperty
from kivy.graphics import Color
from formTypes import Forms
from Form_class import WB_Line, WB_Rectangle, WB_Square, WB_Ellipse, WB_Circle, Point

line_width = 5
client_form_database = {}
form_number = 0
client_id = "yoann"


class WhiteboardInstance(RelativeLayout):
    """Class defining the Widget that the user can draw on"""

    touch_origin_x = NumericProperty(0)
    touch_origin_y = NumericProperty(0)

    def __init__(self, sending_queue):
        super().__init__()
        self.drawing = False
        self._selected_form = None
        self.sending_queue = sending_queue
        with self.canvas:
            self.back = Rectangle(pos=(0, 0), size=(self.width, self.height))
            Color(rgba=(1, 0, 0, 1))

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, value, three):
        self.back.pos = self.pos
        self.back.size = self.size

    def on_touch_down(self, touch):
        self.drawing = True
        self.touch_origin_x = touch.x
        self.touch_origin_y = touch.y
        print("down", touch.x, touch.y)

        with self.canvas:
            if self._selected_form == Forms.LINE:
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=line_width)
            elif self._selected_form == Forms.RECT:
                touch.ud['rect'] = Rectangle(
                    pos=(touch.x, touch.y),
                    size=(0, 0))
            elif self._selected_form == Forms.SQUARE:
                touch.ud['square'] = Rectangle(
                    pos=(touch.x, touch.y),
                    size=(0, 0))
            elif self._selected_form == Forms.ELLIPSE:
                touch.ud['ellipse'] = Ellipse(
                    pos=(touch.x, touch.y),
                    size=(0, 0))
            elif self._selected_form == Forms.CIRCLE:
                touch.ud['circle'] = Ellipse(
                    pos=(touch.x, touch.y),
                    size=(0, 0))
        return True

    def on_touch_move(self, touch):

        if self.collide_point(touch.x, touch.y):
            if self._selected_form == Forms.LINE:
                if len(touch.ud['line'].points) <= 2:
                    touch.ud['line'].points += (touch.x, touch.y)
                else:
                    del touch.ud['line'].points[-2:]
                    touch.ud['line'].points += [touch.x, touch.y]

            elif self._selected_form == Forms.RECT:
                touch.ud['rect'].size = touch.x - self.touch_origin_x, \
                    touch.y - self.touch_origin_y

            elif self._selected_form == Forms.SQUARE:
                dx = touch.x - self.touch_origin_x
                dy = touch.y - self.touch_origin_y
                l = max(abs(dx), abs(dy))
                sign = lambda x: (1, -1)[x < 0]
                touch.ud['square'].size = sign(dx) * l, sign(dy) * l

            elif self._selected_form == Forms.ELLIPSE:
                touch.ud['ellipse'].size = touch.x - self.touch_origin_x, \
                    touch.y - self.touch_origin_y

            elif self._selected_form == Forms.CIRCLE:
                dx = touch.x - self.touch_origin_x
                dy = touch.y - self.touch_origin_y
                l = max(abs(dx), abs(dy))
                sign = lambda x: (1, -1)[x < 0]
                touch.ud['circle'].size = sign(dx) * l, sign(dy) * l

        return True

    def on_touch_up(self, touch):
        self.drawing = False
        global client_form_database
        global form_number


        if self._selected_form == Forms.LINE:
            # prevents key error if for some reason the first click has not
            # created a line object
            if 'line' in touch.ud:
                del touch.ud['line'].points[-2:]
                print('removing last point, line : ', touch.ud['line'].points)
                touch.ud['line'].points += [touch.x, touch.y]

                a = Point(int(self.touch_origin_x), int(self.touch_origin_y))
                b = Point(int(touch.x), int(touch.y))
                form_number += 1
                client_form_database[client_id + str(form_number)] = \
                    WB_Line(a, b, identifier=client_id + str(form_number))
                self.sending_queue.put(WB_Line(a, b, identifier=client_id +
                                       str(form_number)).get_string())

        elif self._selected_form == Forms.RECT:
            a = Point(int(self.touch_origin_x), int(self.touch_origin_y))
            b = Point(int(touch.x), int(touch.y))
            form_number += 1
            client_form_database[client_id + str(form_number)] = \
                WB_Rectangle(a, b, identifier=client_id + str(form_number))
            self.sending_queue.put(WB_Rectangle(a, b, identifier=client_id +
                                               str(form_number)).get_string())

        elif self._selected_form == Forms.SQUARE:
            dx = touch.x - self.touch_origin_x
            dy = touch.y - self.touch_origin_y
            l = int(max(abs(dx), abs(dy)))
            # take the bottom left corner so the coordinates will be positive
            # the square object takes only positive coordinates
            x_min = min(int(touch.x), int(self.touch_origin_x))
            y_min = min(int(touch.y), int(self.touch_origin_y))
            a = Point(x_min, y_min)
            b = Point(x_min + l, y_min + l)
            form_number += 1
            client_form_database[client_id + str(form_number)] = \
                WB_Square(a, b, identifier=client_id + str(form_number))
            self.sending_queue.put(WB_Square(a, b, identifier=client_id +
                                             str(form_number)).get_string())

        elif self._selected_form == Forms.ELLIPSE:
            c = Point(
                int((touch.x + self.touch_origin_x) / 2),
                int((touch.y + self.touch_origin_y) / 2))
            rx = int(abs(touch.x - self.touch_origin_x) /2 )
            ry = int(abs(touch.y - self.touch_origin_y) /2 )
            form_number += 1
            client_form_database[client_id + str(form_number)] = \
                WB_Ellipse(c, rx, ry, identifier=client_id + str(form_number))
            self.sending_queue.put(WB_Ellipse(c, rx, ry, identifier=client_id +
                                              str(form_number)).get_string())

        elif self._selected_form == Forms.CIRCLE:
            c = Point(
                int((touch.x + self.touch_origin_x) / 2),
                int((touch.y + self.touch_origin_y) / 2))
            r = int(abs(touch.x - self.touch_origin_x) / 2)
            form_number += 1
            client_form_database[client_id + str(form_number)] = \
                WB_Circle(c, r, identifier=client_id + str(form_number))
            self.sending_queue.put(WB_Circle(c, r, identifier=client_id +
                                             str(form_number)).get_string())

        return True

    def draw_form(self, form):

        with self.canvas:
            if isinstance(form, WB_Line):
                Line(points=(
                    form.a.x,
                    form.a.y,
                    form.b.x,
                    form.b.y),
                    width= line_width)

            elif isinstance(form, WB_Rectangle):
                Rectangle(pos=(form.a.x, form.a.y),
                          size=(form.b.x - form.a.x, form.b.y - form.a.y))

            elif isinstance(form, WB_Square):
                Rectangle(pos=(form.a.x, form.a.y),
                          size=(form.b.x - form.a.x, form.b.y - form.a.y))

            elif isinstance(form, WB_Circle):
                Ellipse(pos=(form.c.x - form.r, form.c.y - form.r),
                          size=(form.r * 2, form.r * 2))

            elif isinstance(form, WB_Ellipse):
                Ellipse(pos=(form.c.x - form.rx / 2, form.c.y - form.ry /2),
                          size=(form.rx * 2 , form.ry * 2))




    @property
    def selected_form(self):
        return self._selected_form

    @selected_form.setter
    def selected_form(self, selected=None):
        self._selected_form = selected

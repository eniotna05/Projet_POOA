
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle, Line, Ellipse
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ListProperty
from kivy.graphics import Color
from kivy.uix.image import Image
from formTypes import Forms
from Form_class import WB_Line, WB_Rectangle, \
    WB_Square, WB_Ellipse, WB_Circle, WB_Label, Point, Pic
from Command_class import Delete_demend

from Form_class import LINE_WIDTH


class WhiteboardInstance(RelativeLayout):
    """Class defining the Widget that the user can draw on"""

    touch_origin_x = NumericProperty(0)
    touch_origin_y = NumericProperty(0)
    drawing_color = ListProperty([1,0,0,1])

    def __init__(self, sending_queue, session_manager):
        super().__init__()
        self.drawing = False
        self._selected_form = None
        self.sending_queue = sending_queue
        self.session_manager = session_manager
        self.__label_index = {}
        self._open_popup = True

        with self.canvas:
            self.back = Rectangle(pos=(0, 0), size=(self.width, self.height))
            Color(rgba=(1,0,0,1))

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, value, three):
        """Function called whe resizing the window to ensure the white
        background is also resized
        """
        self.back.pos = self.pos
        self.back.size = self.size

    def on_touch_down(self, touch):
        self.drawing = True
        self.touch_origin_x = touch.x
        self.touch_origin_y = touch.y
        print("down", touch.x, touch.y)

        with self.canvas:
            Color(rgba=self.drawing_color)
            if self._selected_form == Forms.LINE:
                touch.ud['line'] = Line(points=(touch.x, touch.y),
                                        width=LINE_WIDTH)
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
            elif self._selected_form == Forms.IMAGE:
                touch.ud['image'] = Image(
                    source="./images/snice.png",
                    pos=(touch.x, touch.y))
            elif self._selected_form == Forms.TEXT:
                touch.ud['text'] = Rectangle(
                    pos=(touch.x, touch.y),
                    size=(0, 0),
                    group='tmp_text_rectangle')

        if self._selected_form == Forms.DELETE:
            # We return the top (last created) form
            # that includes the point we clicked
            result = self.session_manager.extract_top_form(touch.x, touch.y)
            print(result)
            if not result:
                pass
            else:
                # We check if this form was created by us
                #  if it is, deletion is immediate
                # if not permission is asked to owner
                if self.session_manager.client_id == \
                        result.identifier.split("-")[0]:
                    self.delete_form_in_canvas(result.identifier, "int")
                else:
                    self.sending_queue.put(
                        Delete_demend(result.identifier,
                                      self.session_manager.client_id ).get_string())
                    print("""This form belongs to {}. Authorization to
                    delete is being asked
                    """.format(result.identifier.split("-")[0]))

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

            elif self._selected_form == Forms.TEXT:
                touch.ud['text'].size = touch.x - self.touch_origin_x, \
                    touch.y - self.touch_origin_y

        return True

    def on_touch_up(self, touch):

        # Sometimes on_touch_up is fired
        # even if on_touch_down has not been fired
        # This condition prevents from drawing a form in this case.
        if self.drawing:

            if self._selected_form == Forms.LINE:
                # prevents key error if for some reason
                # the first click has not
                # created a line object
                if 'line' in touch.ud:
                    del touch.ud['line'].points[-2:]
                    print('removing last point, line : ',
                                    touch.ud['line'].points)
                    touch.ud['line'].points += [touch.x, touch.y]

                    a = Point(int(self.touch_origin_x), int(
                                        self.touch_origin_y))
                    b = Point(int(touch.x), int(touch.y))
                    group_name = self.session_manager.store_internal_form(
                                                            WB_Line(a, b))
                    touch.ud['line'].group = group_name


            elif self._selected_form == Forms.RECT:
                a = Point(int(self.touch_origin_x), int(self.touch_origin_y))
                b = Point(int(touch.x), int(touch.y))
                group_name = self.session_manager.store_internal_form(
                                                    WB_Rectangle(a, b))
                touch.ud['rect'].group = group_name


            elif self._selected_form == Forms.SQUARE:
                dx = touch.x - self.touch_origin_x
                dy = touch.y - self.touch_origin_y
                l = int(max(abs(dx), abs(dy)))
                # take the bottom left corner
                # so the coordinates will be positive
                # the square object takes only positive coordinates
                x_min = min(int(touch.x), int(self.touch_origin_x))
                y_min = min(int(touch.y), int(self.touch_origin_y))
                a = Point(x_min, y_min)
                b = Point(x_min + l, y_min + l)
                group_name = self.session_manager.store_internal_form(
                                                        WB_Square(a, b))
                touch.ud['square'].group = group_name

            elif self._selected_form == Forms.ELLIPSE:
                c = Point(
                    int((touch.x + self.touch_origin_x) / 2),
                    int((touch.y + self.touch_origin_y) / 2))
                rx = int(abs(touch.x - self.touch_origin_x) /2 )
                ry = int(abs(touch.y - self.touch_origin_y) /2 )
                group_name = self.session_manager.store_internal_form(
                                                WB_Ellipse(c, rx, ry))
                touch.ud['ellipse'].group = group_name


            elif self._selected_form == Forms.CIRCLE:
                c = Point(
                    int((touch.x + self.touch_origin_x) / 2),
                    int((touch.y + self.touch_origin_y) / 2))
                r = int(abs(touch.x - self.touch_origin_x) / 2)
                group_name = self.session_manager.store_internal_form(
                                                        WB_Circle(c, r))
                touch.ud['circle'].group = group_name

            elif self.selected_form == Forms.IMAGE:
                a = Point(int(self.touch_origin_x), int(self.touch_origin_y))
                group_name = self.session_manager.store_internal_form(Pic(a))
                touch.ud['image'].group = group_name

            elif self.selected_form == Forms.TEXT:
                # ask usr for text input
                text_input = 'CONTENU'
                self.canvas.remove_group('tmp_text_rectangle')

                a = Point(int(self.touch_origin_x), int(self.touch_origin_y))
                b = Point(int(touch.x), int(touch.y))

                group_id = self.session_manager.store_internal_form(
                    WB_Label(a, b, text_input))

                with self.canvas:
                    label = Label(text=text_input,
                                  color=(1, 0, 0, 1),
                                  size=(touch.x - self.touch_origin_x,
                                        touch.y - self.touch_origin_y),
                                  pos=(self.touch_origin_x, self.touch_origin_y))
                label.canvas.group = group_id

        self.drawing = False

        return True

    def draw_form(self, form):

        with self.canvas:

            if isinstance(form, WB_Line):
                group_name = self.session_manager.store_external_form(form)
                Line(points=(
                    form.a.x,
                    form.a.y,
                    form.b.x,
                    form.b.y),
                    width= LINE_WIDTH, group = group_name)

            elif isinstance(form, WB_Rectangle):
                group_name = self.session_manager.store_external_form(form)
                Rectangle(pos=(form.a.x, form.a.y),
                          size=(form.b.x - form.a.x, form.b.y - form.a.y),
                          group = group_name)

            elif isinstance(form, WB_Square):
                group_name = self.session_manager.store_external_form(form)
                Rectangle(pos=(form.a.x, form.a.y),
                          size=(form.b.x - form.a.x, form.b.y - form.a.y),
                        group = group_name)

            elif isinstance(form, WB_Circle):
                group_name = self.session_manager.store_external_form(form)
                Ellipse(pos=(form.c.x - form.r, form.c.y - form.r),
                          size=(form.r * 2, form.r * 2),group = group_name)

            elif isinstance(form, WB_Ellipse):
                group_name = self.session_manager.store_external_form(form)
                Ellipse(pos=(form.c.x - form.rx / 2, form.c.y - form.ry /2),
                        size=(form.rx * 2 , form.ry * 2), group = group_name)

            elif isinstance(form, WB_Label):
                group_id = self.session_manager.store_external_form(form)
                label = Label(text=form.text_input,
                              color=(1, 0, 0, 1),
                              size=(form.b.x - form.a.x, form.b.y - form.a.y),
                              pos=(form.a.x, form.a.y))
                label.canvas.group = group_id

            elif isinstance(form, Pic):
                group_name = self.session_manager.store_external_form(form)
                Image(source='./images/snice.png',
                      pos=(form.c.x, form.c.y), group = group_name)

    def delete_form_in_canvas(self, form_id, source):

        self.canvas.remove_group(form_id)
        self.session_manager.delete_form(form_id, source)

    @property
    def selected_form(self):
        return self._selected_form

    @selected_form.setter
    def selected_form(self, selected=None):
        self._selected_form = selected

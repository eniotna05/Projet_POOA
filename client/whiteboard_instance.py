from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle, Line, Ellipse
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ListProperty
from kivy.graphics import Color
from kivy.uix.image import Image

from time import sleep

from utils.form_types import Forms
from utils.form_class import WBLine, WBRectangle, WBSquare, WBEllipse, \
    WBCircle, WBPoint, WBPicture, WBLabel, LINE_WIDTH, STICKER_SIZE, STICKER_URL

from utils.command_class import DeleteRequest


class WhiteboardInstance(RelativeLayout):
    """Class defining the Widget that the user can draw on. The important
    element of this Widget is the kivy canvas, a set of instructions telling the
    library how to draw the forms."""

    # These are kivy properties, with automatic biding (board is updated when
    # they change) and accessors
    touch_origin_x = NumericProperty(0)
    touch_origin_y = NumericProperty(0)
    drawing_color = ListProperty([1, 0, 0, 1])

    def __init__(self, sending_queue, session_manager):
        super().__init__()
        self.drawing = False
        self._selected_form = None
        self.sending_queue = sending_queue
        self.session_manager = session_manager

        with self.canvas:
            self.back = Rectangle(pos=(0, 0), size=(self.width, self.height))
            Color(rgba=(1, 0, 0, 1))

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, value, three):
        """Method called whe resizing the window to ensure the white
        background is also resized."""
        self.back.pos = self.pos
        self.back.size = self.size

    def on_touch_down(self, touch):
        """Method called when the user clicks somewhere in the widget"""
        self.drawing = True
        self.touch_origin_x = touch.x
        self.touch_origin_y = touch.y

        # Kivy objects are automatically added to the canvas
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
                a = WBPoint(int(touch.x - STICKER_SIZE / 2),
                          int(touch.y - STICKER_SIZE / 2))
                touch.ud['image'] = Image(
                    source=STICKER_URL,
                    pos=(touch.x - STICKER_SIZE / 2, touch.y - STICKER_SIZE / 2),
                    size=(STICKER_SIZE, STICKER_SIZE))

                group_name = self.session_manager.store_internal_form(WBPicture(a))
                touch.ud['image'].canvas.group = group_name

            elif self._selected_form == Forms.TEXT:
                touch.ud['text'] = Rectangle(
                    pos=(touch.x, touch.y),
                    size=(0, 0),
                    group='tmp_text_rectangle')

        if self._selected_form == Forms.DELETE:
            # We return the top (last created) form
            # that includes the point we clicked
            result = self.session_manager.extract_top_form(touch.x, touch.y)

            if result is not None:
                # We check if this form was created by us
                #  if it is, deletion is immediate
                # if not permission is asked to owner
                if self.session_manager.client_id == \
                        result.identifier.split("-")[0]:
                    self.delete_form_in_canvas(result.identifier, send_to_server=True)
                else:
                    self.sending_queue.put(
                        DeleteRequest(result.identifier,
                                      self.session_manager.client_id ).get_string())
                    print("""This form belongs to {}. Authorization to
                    delete is being asked
                    """.format(result.identifier.split("-")[0]))

        return True

    def on_touch_move(self, touch):
        """Method called after on_touch_down. touch is an object with
        the current coordinates of the mouse / finger position"""

        # we check if we are inside the drawing area
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
        """Method called after on_touch_move. touch is an object with
        the current coordinates of the mouse / finger position"""

        # Sometimes on_touch_up is fired even if on_touch_down has not been
        # fired. This condition prevents from drawing a form in this case.
        if self.drawing:

            if self._selected_form == Forms.LINE:
                # prevents key error if for some reason the first click has not
                # created a line object
                if 'line' in touch.ud:
                    del touch.ud['line'].points[-2:]
                    touch.ud['line'].points += [touch.x, touch.y]

                    a = WBPoint(int(self.touch_origin_x),
                              int(self.touch_origin_y))
                    b = WBPoint(int(touch.x), int(touch.y))
                    group_name = \
                        self.session_manager.store_internal_form(WBLine(a, b))
                    touch.ud['line'].group = group_name

            elif self._selected_form == Forms.RECT:
                a = WBPoint(int(self.touch_origin_x), int(self.touch_origin_y))
                b = WBPoint(int(touch.x), int(touch.y))
                group_name = \
                    self.session_manager.store_internal_form(WBRectangle(a, b))
                touch.ud['rect'].group = group_name

            elif self._selected_form == Forms.SQUARE:
                dx = touch.x - self.touch_origin_x
                dy = touch.y - self.touch_origin_y
                l = int(max(abs(dx), abs(dy)))

                # take the bottom left corner so the coordinates will be positive
                # the square object takes only positive coordinates
                x_min = min(int(touch.x), int(self.touch_origin_x))
                y_min = min(int(touch.y), int(self.touch_origin_y))
                a = WBPoint(x_min, y_min)
                b = WBPoint(x_min + l, y_min + l)
                group_name = \
                    self.session_manager.store_internal_form(WBSquare(a, b))
                touch.ud['square'].group = group_name

            elif self._selected_form == Forms.ELLIPSE:
                c = WBPoint(int((touch.x + self.touch_origin_x) / 2),
                          int((touch.y + self.touch_origin_y) / 2))
                rx = int(abs(touch.x - self.touch_origin_x) / 2)
                ry = int(abs(touch.y - self.touch_origin_y) / 2)
                group_name = \
                    self.session_manager.store_internal_form(WBEllipse(c, rx, ry))
                touch.ud['ellipse'].group = group_name

            elif self._selected_form == Forms.CIRCLE:
                c = WBPoint(int((touch.x + self.touch_origin_x) / 2),
                          int((touch.y + self.touch_origin_y) / 2))
                r = int(abs(touch.x - self.touch_origin_x) / 2)
                group_name = \
                    self.session_manager.store_internal_form(WBCircle(c, r))
                touch.ud['circle'].group = group_name

            elif self.selected_form == Forms.TEXT:
                # ask usr for text input
                text_input = 'CONTENU'
                self.canvas.remove_group('tmp_text_rectangle')

                a = WBPoint(int(self.touch_origin_x), int(self.touch_origin_y))
                b = WBPoint(int(touch.x), int(touch.y))

                group_id = self.session_manager.store_internal_form(
                    WBLabel(a, b, text_input))

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
        """Method calld to draw a form on the board andd add it to the local
        storage. It is especilly usefull when receiving a from from the network"""

        with self.canvas:


            if isinstance(form, WBLine):
                group_name = self.session_manager.store_external_form(form)
                Line(points=(form.a.x, form.a.y, form.b.x, form.b.y),
                     width=LINE_WIDTH,
                     group=group_name)

            elif isinstance(form, WBRectangle):
                group_name = self.session_manager.store_external_form(form)
                Rectangle(pos=(form.a.x, form.a.y),
                          size=(form.b.x - form.a.x, form.b.y - form.a.y),
                          group=group_name)

            elif isinstance(form, WBSquare):
                group_name = self.session_manager.store_external_form(form)
                Rectangle(pos=(form.a.x, form.a.y),
                          size=(form.b.x - form.a.x, form.b.y - form.a.y),
                          group=group_name)

            elif isinstance(form, WBCircle):
                group_name = self.session_manager.store_external_form(form)
                Ellipse(pos=(form.c.x - form.r, form.c.y - form.r),
                        size=(form.r * 2, form.r * 2),
                        group=group_name)

            elif isinstance(form, WBEllipse):
                group_name = self.session_manager.store_external_form(form)
                Ellipse(pos=(form.c.x - form.rx / 2, form.c.y - form.ry / 2),
                        size=(form.rx * 2, form.ry * 2),
                        group=group_name)

            elif isinstance(form, WBLabel):
                group_id = self.session_manager.store_external_form(form)
                label = Label(text=form.text_input,
                              color=(1, 0, 0, 1),
                              size=(form.b.x - form.a.x, form.b.y - form.a.y),
                              pos=(form.a.x, form.a.y))
                label.canvas.group = group_id

            elif isinstance(form, WBPicture):
                group_name = self.session_manager.store_external_form(form)
                image = Image(source=STICKER_URL,
                              pos=(form.c.x, form.c.y),
                              size=(STICKER_SIZE, STICKER_SIZE))
                image.canvas.group = group_name
            print(len(self.canvas.children))

    def delete_form_in_canvas(self, form_id, send_to_server=False):
        """Method called to remove a form from the canvas and from the local
        storage"""

        self.canvas.remove_group(form_id)
        self.session_manager.delete_form(form_id, send_to_server)

    @property
    def selected_form(self):
        return self._selected_form

    @selected_form.setter
    def selected_form(self, selected=None):
        self._selected_form = selected

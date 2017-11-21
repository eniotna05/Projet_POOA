# File defining the custom forms used in the application.
# The get_string methods are usually called to transform the objects into
# strings that can be transferred over the socket.
# The check_inclusion methods are called to check if a point is in the area
#  of a form

ABSCISS_MAX = 10000
ORDINATE_MAX = 10000
LINE_WIDTH = 5
STICKER_SIZE = 50
STICKER_URL = './images/snice.png'


class WBColor:
    """ parameters are colors HTML RGBA codes in that order (A is alpha
    channel), and are coded on 8bits"""

    def __init__(self, R, G, B, A):
        if not isinstance(R, int) or not isinstance(G, int) or \
                not isinstance(B, int) or not isinstance(A, int):
            raise TypeError("All parameters have to be interger")

        if not 0 <= R <= 255 or not 0 <= G <= 255 or not 0 <= B <= 255 or \
                not 0 <= A <= 255:
            raise ValueError("All parameters have to be between 0 and 255")

        self._R = R
        self._G = G
        self._B = B
        self._A = A

    def __repr__(self):
        return """Color of RGBA code: {}.{}.{}.{}""".format(self._R, self._G,
                                                            self._B, self._A)

    def get_string(self):
        return str(self._R) + "," + str(self._G) + "," + str(self._B) + "," + \
            str(self._A)

    def get_relative_values(self):
        return [self._R / 255, self._G / 255, self._B / 255, self._A / 255]

    @staticmethod
    def to_8bit(relative_values):
        """Static utilitary function that converts an array of relative values
        of RGBA code into values between 0 and 255"""
        for v in relative_values:
            if not isinstance(v, float):
                raise TypeError("All channels have to be floats")
            if not 0 <= v <= 1:
                raise ValueError("Channel must be relative between 0 and 1")

        return [int(255 * v) for v in relative_values]

    @staticmethod
    def to_relative_code(bit_values):
        """Static utilitary function that converts an array of 8bit RGBA values
        into an array of relative values between 0 and 1"""
        for v in bit_values:
            if not isinstance(v, int):
                raise TypeError("All channels have to be integer")
            if not 0 <= v <= 255:
                raise ValueError("Channel must be between 0 and 255")

        return [v / 255 for v in bit_values]


BLACK = WBColor(0, 0, 0, 1)


class WBPoint:
    """ x and y are the absciss and ordinate of the point on the white board
    they have to be integer and have a max value depending on the board size
    and a min value of zero
    """

    def __init__(self, x, y):
        if not isinstance(x, int):
            raise TypeError("THe first parameter has to be an integer")
        if not isinstance(y, int):
            raise TypeError("Le second parameter has to be an integer")
        if x > ABSCISS_MAX:
            raise ValueError("The absciss is too high")
        if x < 0:
            raise ValueError("THe absciss has to be positive")
        if y > ORDINATE_MAX:
            raise ValueError("The ordinate is too high")
        if y < 0:
            raise ValueError("The ordinate has to be positive")

        self._x = x
        self._y = y

    def __repr__(self):
        return """Point of absciss {} and ordinate {}""".format(self._x,
                                                                self._y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class WBForm:
    """Base class from which other forms inherit"""

    def __init__(self, color=BLACK, identifier=0):
        self._identifier = identifier
        self._color = color

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, iden):
        self._identifier = iden

    @property
    def color(self):
        return self._color


class WBLine(WBForm):
    """ a and b are the two tip points of the line"""

    def __init__(self, a, b, color=BLACK, identifier=0):
        super().__init__(color=color, identifier=identifier)
        if not isinstance(a, WBPoint):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(b, WBPoint):
            raise TypeError("The second parameter has to be a point")
        if not isinstance(color, WBColor):
            raise TypeError("The third parameter has to be a color")

        self._a = a
        self._b = b

    def __repr__(self):
        return """Lign from {} to {} and of color: {} and of 
        id: {}""".format(self._a, self._b, self._color, self._identifier)

    def get_string(self):
        """method to transform lign into string
        Ex: lign from (2,4) to (8,14) => string = L2,4,8,14"""
        string = "L" + str(self._a.x) + "," + str(self._a.y) + ","
        string += str(self._b.x) + "," + str(self._b.y) + ","
        string += self._color.get_string() + "," + str(self._identifier)
        return string

    def check_inclusion(self, x_selection, y_selection):
        """method to check if selected point (x_selection, y_selection)
         is inside the line"""
        # This code determines the cordinates of c:
        # the intersection point between the line
        # and the perpendicular line crossing the selection point
        # We have to deal with some specific cases
        #  to avoid division by zero error
        print(x_selection, y_selection)

        if self._a.x < self._b.x:
            point1 = self._a
            point2 = self._b
        else:
            point1 = self._b
            point2 = self._a

        # Special case 1: the line is parallel to the ordinate line
        if point2.x == point1.x:
            if point2.x - x_selection <= LINE_WIDTH:
                return True
            else:
                return False

        # Special case 2: the line is parallel to the absiss line
        if point2.y == point1.y:
            if point2.y - y_selection <= LINE_WIDTH:
                return True
            else:
                return False

        a1 = (point2.y - point1.y) / (point2.x - point1.x)
        b1 = point1.y - a1 * point1.x
        a2 = -1 / a1
        b2 = y_selection - a2 * x_selection
        cx = (b2 - b1) / (a1 - a2)
        cy = cx * a1 + b1

        # Now we check if the distance between this point and selection
        # point is less than LINE_WIDTH parameter
        # (which is half of actual line with)
        if (cy - y_selection)**2 + (cx - x_selection)**2 <= (LINE_WIDTH)**2:
            return True
        else:
            return False


    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b


class WBRectangle(WBForm):
    """a is one of the summit of the rectangle,
    b is the summit on the other side of the diagonal"""

    def __init__(self, a, b, color=BLACK, identifier=0):
        super().__init__(color=color, identifier=identifier)
        if not isinstance(a, WBPoint):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(b, WBPoint):
            raise TypeError("The second parameter has to be a point")
        if not isinstance(color, WBColor):
            raise TypeError("The third parameter has to be a color")
        self._a = a
        self._b = b

    def __repr__(self):
        return """Rectangle from {} to {} and of color: {} and of id:
         {}""".format(self._a, self._b, self._color, self._identifier)

    def get_string(self):
        """method to transform rectangle into string
        Ex: rectangle from (2,4) to (8,14) => string = R2,4,8,14"""
        string = "R" + str(self._a.x) + "," + str(self._a.y) + ","
        string += str(self._b.x) + "," + str(self._b.y) + ","
        string += self._color.get_string() + "," + str(self._identifier)
        return string

    def check_inclusion(self, x_selection, y_selection):
        """method to check if selected point (x_selection, y_selection)
         is inside the rectange"""
        if x_selection < max(self._a.x, self._b.x) and \
           x_selection > min(self._a.x, self._b.x) and \
           y_selection < max(self._a.y, self._b.y) and \
           y_selection > min(self._a.y, self._b.y):
            return True
        else:
            return False

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b


class WBSquare(WBForm):

    """a is one of the summit of the square,
    b is the summit on the other side of the diagonal
    """
    def __init__(self, a, b, color=BLACK, identifier=0):
        super().__init__(color=color, identifier=identifier)
        if not isinstance(a, WBPoint):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(b, WBPoint):
            raise TypeError("The second parameter has to be a point")
        if not isinstance(color, WBColor):
            raise TypeError("The third parameter has to be a color")
        if abs(a.x - b.x) != abs(a.y - b.y):
            raise ValueError("This is not a square !!!!")
        self._a = a
        self._b = b

    def __repr__(self):
        return """Square of corners {} and {} and of color: {} and of 
        id: {}""".format(self._a, self._b, self._color, self._identifier)

    def get_string(self):
        """method to transform square into string
        Ex: rectangle of left upper corner (17,5) and of side length 2 =>
        string = "S17,5,2"""
        string = "S" + str(self._a.x) + "," + str(self._a.y)
        string += "," + str(self._b.x) + "," + str(self._b.y) + ","
        string += self._color.get_string() + "," + str(self._identifier)
        return string

    def check_inclusion(self, x_selection, y_selection):
        """method to check if selected point (x_selection, y_selection)
         is inside the square"""
        if x_selection < max(self._a.x, self._b.x) and \
           x_selection > min(self._a.x, self._b.x) and \
           y_selection < max(self._a.y, self._b.y) and \
           y_selection > min(self._a.y, self._b.y):
            return True
        else:
            return False

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b


class WBCircle(WBForm):
    """c is the center of the circle, r is the radius   """

    def __init__(self, c, r, color=BLACK, identifier=0):
        super().__init__(color=color, identifier=identifier)
        if not isinstance(c, WBPoint):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(r, int):
            raise TypeError("The second parameter has to be an integer")
        if not isinstance(color, WBColor):
            raise TypeError("The third parameter has to be a color")
        self._c = c
        self._r = r

    def __repr__(self):
        return """Circle of center {}, of radius: {} and of color: {} and of 
        id: {}""".format(self._c, self._r, self._color, self._identifier)

    def get_string(self):
        """method to transform circle into string
        Ex: Circle of center (17,5) and of radius 2 => string = S17,5,2"""
        string = "C" + str(self._c.x) + "," + str(self._c.y)
        string += "," + str(self._r) + ","
        string += self._color.get_string() + "," + str(self._identifier)
        return string

    def check_inclusion(self, x_selection, y_selection):
        """method to check if selected point (x_selection, y_selection)
         is inside the circle"""
        if (x_selection - self._c.x)**2 + \
                        (y_selection - self._c.y)**2 < self._r**2:
            return True
        else:
            return False

    @property
    def c(self):
        return self._c

    @property
    def r(self):
        return self._r


class WBEllipse(WBForm):
    """c is the center of the ellipse, rx is the length of the horizontal
    radius, ry is the length of the vertical radius
    """

    def __init__(self, c, rx, ry, color=BLACK, identifier=0):
        super().__init__(color=color, identifier=identifier)
        if not isinstance(c, WBPoint):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(rx, int):
            raise TypeError("The second parameter has to be an integer")
        if not isinstance(ry, int):
            raise TypeError("The second parameter has to be an integer")
        if not isinstance(color, WBColor):
            raise TypeError("The third parameter has to be a color")

        self._c = c
        self._rx = rx
        self._ry = ry

    def __repr__(self):
        return """Ellipse of center {}, of horizontal radius: {},
        of vertical radius: {} and of color: {} and of id: {}
        """.format(self._c, self._rx, self._ry, self._color, self._identifier)

    def get_string(self):
        """method to transform circle into string
        Ex: Ellipse of center (17,5) and of horizontal radius 7
        and of vertical radius 3 => string = "S17,5,7,3"""
        string = "E" + str(self._c.x) + "," + str(self._c.y)
        string += "," + str(self._rx) + "," + str(self._ry) + ","
        string += self._color.get_string() + "," + str(self._identifier)
        return string

    def check_inclusion(self, x_selection, y_selection):
        """method to check if selected point (x_selection, y_selection)
         is inside the circle"""
        if (x_selection - self._c.x)**2 / self._rx**2 + \
                (y_selection - self._c.y)**2 / self._ry**2 < 1:
            return True
        else:
            return False

    @property
    def c(self):
        return self._c

    @property
    def rx(self):
        return self._rx

    @property
    def ry(self):
        return self._ry


class WBPicture(WBForm):
    """c is the left bottom point of the pic (Image size is a fixed parameter)
    """

    def __init__(self, c, identifier=0):
        super().__init__(identifier=identifier)
        if not isinstance(c, WBPoint):
            raise TypeError("The first parameter has to be an integer")
        self._c = c

    def get_string(self):
        string = "P" + str(self._c.x) + "," + str(self._c.y) + ","
        string += str(self._identifier)
        return string

    def __repr__(self):
        return """Image of center {} and of id {}
        """.format(self._c, self._identifier)

    def check_inclusion(self, x_selection, y_selection):
        """method to check if selected point (x_selection, y_selection)
         is inside the rectange"""
        if x_selection < self._c.x + STICKER_SIZE and \
           x_selection > self._c.x and \
           y_selection < self._c.y + STICKER_SIZE and \
           y_selection > self._c.y:
            return True
        else:
            return False

    @property
    def c(self):
        return self._c


class WBLabel(WBForm):
    """a is one of the corner of the label, b is the diagonal corner
     text_input is the content of the lable (a string)
        """

    def __init__(self, a, b, text_input, color=BLACK, identifier=0):
        super().__init__(color=color, identifier=identifier)
        if not isinstance(a, WBPoint):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(b, WBPoint):
            raise TypeError("The second parameter has to be a point")
        if not isinstance(text_input, str):
            raise TypeError("The third parameter has to be a string")

        self._a = a
        self._b = b
        self._text_input = text_input

    def get_string(self):
        return "T" + str(self._a.x) + "," + str(self._a.y) + "," + \
            str(self._b.x) + "," + str(self._b.y) + "," + \
            self._text_input + "," + self._color.get_string() + "," + \
            str(self._identifier)

    def check_inclusion(self, x_selection, y_selection):
        """method to check if selected point (x_selection, y_selection)
         is inside the rectangle defining the label"""
        if x_selection < max(self._a.x, self._b.x) and \
           x_selection > min(self._a.x, self._b.x) and \
           y_selection < max(self._a.y, self._b.y) and \
           y_selection > min(self._a.y, self._b.y):
            return True
        else:
            return False

    def __repr__(self):
        return """Label of point {} to point {} of color {} and content
         '{}' and of id: {}.""".format(self._a, self._b,
                        self._color, self._text_input, self._identifier)

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    def text_input(self):
        return self._text_input

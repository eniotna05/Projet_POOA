# File defining the forms that can be exchanged over the network

ABSCISS_MAX = 10000
ORDINATE_MAX = 10000
LINE_WIDTH = 5
STICKER_SIZE = 50
STICKER_URL = './images/snice.png'


class WBColor:
    """ parameters are colors HTML RGB codes in that order"""

    def __init__(self, R, G, B):
        if (not isinstance(R, int) or not isinstance(G, int) or
            not isinstance(B, int)):
            raise TypeError("All parameters have to be interger")

        if R < 0 or R > 255 or G < 0 or G > 255 or B < 0 or B > 255:
            raise ValueError("All parameters have to be between 0 and 255")

        self._R = R
        self._G = G
        self._B = B

    def __repr__(self):
        return """Color of RGB code: {}.{}.{}""".format(self._R, self._G, self._B)


BLACK = WBColor(0, 0, 0)


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

    def __init__(self, identifier=0):
        self._identifier = identifier

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, iden):
        self._identifier = iden


class WBLine(WBForm):
    """ a and b are the two tip points of the line"""

    def __init__(self, a, b, color=BLACK, identifier=0):
        super().__init__(identifier=identifier)
        if not isinstance(a, WBPoint):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(b, WBPoint):
            raise TypeError("The second parameter has to be a point")
        if not isinstance(color, WBColor):
            raise TypeError("The third parameter has to be a color")

        self._a = a
        self._b = b
        self._color = color

    def __repr__(self):
        return """Lign from {} to {} and of color: {}
        and of id: {}""".format(self._a, self._b, self._color, self._identifier)

    def get_string(self):
        """method to transform lign into string
        Ex: lign from (2,4) to (8,14) => string = L2,4,8,14"""
        string = "L" + str(self._a.x) + "," + str(self._a.y) + ","
        string += str(self._b.x) + "," + str(self._b.y) + ","
        string += str(self._identifier)
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

    def change_position(self, x, y):
        """method to change position of the form
        horizontal movement = x , vertical movement = y"""
        if not isinstance(x, int):
            raise TypeError("The first parameter has to be an integer")
        if not isinstance(y, int):
            raise TypeError("The second parameter has to be an integer")

        self._a.x += x
        self._b.x += x
        self._a.y += y
        self._b.y += y

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
        super().__init__(identifier=identifier)
        if not isinstance(a, WBPoint):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(b, WBPoint):
            raise TypeError("The second parameter has to be a point")
        if not isinstance(color, WBColor):
            raise TypeError("The third parameter has to be a color")
        self._a = a
        self._b = b
        self._color = color

    def __repr__(self):
        return """Rectangle from {} to {} and of color: {}
        and of id: {}""".format(self._a, self._b, self._color, self._identifier)

    def get_string(self):
        """method to transform rectangle into string
        Ex: rectangle from (2,4) to (8,14) => string = R2,4,8,14"""
        string = "R" + str(self._a.x) + "," + str(self._a.y) + ","
        string += str(self._b.x) + "," + str(self._b.y) + ","
        string += str(self._identifier)
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

    def change_position(self, x, y):
        """method to change position of the form
        horizontal movement = x , vertical movement = y"""
        if not isinstance(x, int):
            raise TypeError("The first parameter has to be an integer")
        if not isinstance(y, int):
            raise TypeError("The second parameter has to be an integer")

        self._a.x += x
        self._b.x += x
        self._a.y += y
        self._b.y += y

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
        super().__init__(identifier=identifier)
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
        self._color = color

    def __repr__(self):
        return """Square of corners {} and {} and of color: {}
        and of id: {}""".format(self._a, self._b, self._color, self._identifier)

    def get_string(self):
        """method to transform square into string
        Ex: rectangle of left upper corner (17,5) and of side length 2 =>
        string = "S17,5,2"""
        string = "S" + str(self._a.x) + "," + str(self._a.y)
        string += "," + str(self._b.x) + "," + str(self._b.y) + ","
        string += str(self._identifier)
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

    def change_position(self, x, y):
        """method to change position of the form
        horizontal movement = x , vertical movement = y"""
        if not isinstance(x, int):
            raise TypeError("The first parameter has to be an integer")
        if not isinstance(y, int):
            raise TypeError("The second parameter has to be an integer")

        self._a.x += x
        self._b.x += x
        self._a.y += y
        self._b.y += y

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b


class WBCircle(WBForm):
    """c is the center of the circle, r is the radius   """

    def __init__(self, c, r, color=BLACK, identifier=0):
        super().__init__(identifier=identifier)
        if not isinstance(c, WBPoint):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(r, int):
            raise TypeError("The second parameter has to be an integer")
        if not isinstance(color, WBColor):
            raise TypeError("The third parameter has to be a color")
        self._c = c
        self._r = r
        self._color = color

    def __repr__(self):
        return """Circle of center {}, of radius: {} and of color: {}
        and of id: {}""".format(self._c, self._r, self._color, self._identifier)

    def get_string(self):
        """method to transform circle into string
        Ex: Circle of center (17,5) and of radius 2 => string = S17,5,2"""
        string = "C" + str(self._c.x) + "," + str(self._c.y)
        string += "," + str(self._r) + ","
        string += str(self._identifier)
        return string

    def check_inclusion(self, x_selection, y_selection):
        """method to check if selected point (x_selection, y_selection)
         is inside the circle"""
        if (x_selection - self._c.x)**2 + (y_selection - self._c.y)**2 < self._r**2:
            return True
        else:
            return False

    def change_position(self, x, y):
        """method to change position of the form
        horizontal movement = x , vertical movement = y"""
        if not isinstance(x, int):
            raise TypeError("The first parameter has to be an integer")
        if not isinstance(y, int):
            raise TypeError("The second parameter has to be an integer")

        self._c.x += x
        self._c.y += y

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
        super().__init__(identifier=identifier)
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
        self._color = color

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
        string += str(self._identifier)
        return string

    def check_inclusion(self, x_selection, y_selection):
        """method to check if selected point (x_selection, y_selection)
         is inside the circle"""
        if (x_selection - self._c.x)**2 / self._rx**2 + \
        (y_selection - self._c.y)**2 / self._ry**2 < 1:
            return True
        else:
            return False

    def change_position(self, x, y):
        """method to change position of the form
        horizontal movement = x , vertical movement = y"""
        if not isinstance(x, int):
            raise TypeError("The first parameter has to be an integer")
        if not isinstance(y, int):
            raise TypeError("The second parameter has to be an integer")

        self._c.x += x
        self._c.y += y

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
    """c is the left bottom point of the pic (Image size is a fixed parameter),
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

    def change_position(self, x, y):
        if not isinstance(x, int):
            raise TypeError("The first parameter has to be an integer")
        if not isinstance(y, int):
            raise TypeError("The first parameter has to be an integer")
        self._c.x += x
        self._c.y += y

    @property
    def c(self):
        return self._c


class WBLabel(WBForm):

    def __init__(self, a, b, text_input, identifier=0):
        super().__init__(identifier=identifier)
        if not isinstance(a, WBPoint):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(text_input, str):
            raise TypeError("The first parameter has to be a string")

        self._a = a
        self._b = b
        self._text_input = text_input

    def get_string(self):
        return "T" + str(self._a.x) + "," + str(self._a.y) + "," + \
            str(self._b.x) + "," + str(self._b.y) + "," + \
            self._text_input + "," + str(self._identifier)

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
        return """Label of point {} to point {} and content '{}'.
        """.format(self._a, self._b, self._text_input)

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b


absciss_max = 10000
ordinate_max = 10000


class Color:

    """ parameters are colors HTML RGB codes in that order"""

    def __init__(self, R, G, B):

        if (not isinstance(R, int) or not isinstance(G, int) or
            not isinstance(B, int)):
            raise TypeError("All parameters have to be interger")
        if R < 0 or R > 255 or G < 0 or G > 255 or B < 0 or B > 255:
            raise ValueError("All parameters have to be between 0 and 255")

        self.R = R
        self.G = G
        self.B = B

    def __repr__(self):

        return """Color of RGB code: {}.{}.{}""".format(self.R, self.G, self.B)


white = Color(255, 255, 255)

black = Color(0, 0, 0)


class Point:

    """ x and y are the absciss and ordinate of the point on the white board
    they have to be integer and have a max value depending on the board size and a min value of zero


    """


    def __init__(self, x, y):

        global absciss_max
        global ordinate_max

        if not isinstance(x, int):
            raise TypeError("THe first parameter has to be an integer")
        if not isinstance(y, int):
            raise TypeError("Le second parameter has to be an integer")
        if x > absciss_max:
            raise ValueError("The absciss is too high")
        if x < 0:
            raise ValueError("THe absciss has to be positive")
        if y > ordinate_max:
            raise ValueError("The ordinate is too high")
        if y < 0:
            raise ValueError("The ordinate has to be positive")

        self.x = x
        self.y = y

    def __repr__(self):

        return """Point of absciss {} and ordinate {}""".format(self.x,
                                                                self.y)


class WB_Form:

    # Classe originelle dont hérite toutes les autres formes
    # Pas utilise en tant que tel pour l'instant

    def __init__(self, *point, identifier=0):
        self.point_list = points
        self.identifier = identifier


class WB_Line(WB_Form):

    """ a and b are the two tip points of the line
    """





    def __init__(self, a, b, color=black, identifier=0):
        if not isinstance(a, Point):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(b, Point):
            raise TypeError("The second parameter has to be a point")
        if not isinstance(color, Color):
            raise TypeError("The third parameter has to be a color")

        self.a = a
        self.b = b
        self.color = color
        self.identifier = identifier

    def __repr__(self):

        return """Lign from {} to {} and of color: {}
        and of id: {}""".format(self.a, self.b, self.color, self.identifier)

    def get_string(self):

        # method to transform lign into string
        # Ex: lign from (2,4) to (8,14) => string = "L2,4,8,14"

        string = "L" + str(self.a.x) + "," + str(self.a.y) + ","
        string += str(self.b.x) + "," + str(self.b.y) + ","
        string += str(self.identifier)
        return string


class WB_Rectangle(WB_Form):

    """a is one of the summit of the rectangle, b is the summit on the other side of the diagonal
    """


    def __init__(self, a, b, color=black, identifier=0):
        if not isinstance(a, Point):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(b, Point):
            raise TypeError("The second parameter has to be a point")
        if not isinstance(color, Color):
            raise TypeError("The third parameter has to be a color")
        self.a = a
        self.b = b
        self.color = color
        self.identifier = identifier

    def __repr__(self):

        return """Rectangle from {} to {} and of color: {}
        and of id: {}""".format(self.a, self.b, self.color, self.identifier)

    def get_string(self):

        # method to transform rectangle into string
        # Ex: rectangle from (2,4) to (8,14) => string = "R2,4,8,14"

        string = "R" + str(self.a.x) + "," + str(self.a.y) + ","
        string += str(self.b.x) + "," + str(self.b.y) + ","
        string += str(self.identifier)
        return string


class WB_Square(WB_Form):

    """a is one of the summit of the square, b is the summit on the other side of the diagonal
    """



    def __init__(self, a, b, color=black, identifier=0):
        if not isinstance(a, Point):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(b, Point):
            raise TypeError("The second parameter has to be a point")
        if not isinstance(color, Color):
            raise TypeError("The third parameter has to be a color")
        if abs(a.x - b.x) != abs(a.y - b.y):
            raise ValueError("This is not a square !!!!")
        self.a = a
        self.b = b
        self.color = color
        self.identifier = identifier

    def __repr__(self):

        return """Square of corners {} and {} and of color: {}
        and of id: {}""".format(self.a, self.b, self.color, self.identifier)

    def get_string(self):

        # method to transform square into string
        # Ex: rectangle of left upper corner (17,5) and of side length 2 =>
        # string = "S17,5,2"

        string = "S" + str(self.a.x) + "," + str(self.a.y)
        string += "," + str(self.b.x) + "," + str(self.b.y) + ","
        string += str(self.identifier)
        return string


class WB_Circle(WB_Form):

    """c is the center of the circle, r is the radius   """
    
    def __init__(self, c, r, color=black, identifier=0):
        if not isinstance(c, Point):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(r, int):
            raise TypeError("The second parameter has to be an integer")
        if not isinstance(color, Color):
            raise TypeError("The third parameter has to be a color")
        self.c = c
        self.r = r
        self.color = color
        self.identifier = identifier

    def __repr__(self):

        return """Circle of center {}, of radius: {} and of color: {}
        and of id: {}""".format(self.c, self.r, self.color, self.identifier)

    def get_string(self):

        # method to transform circle into string
        # Ex: Circle of center (17,5) and of radius 2 => string = "S17,5,2"

        string = "C" + str(self.c.x) + "," + str(self.c.y)
        string += "," + str(self.r) + ","
        string += str(self.identifier)
        return string



class WB_Ellipse(WB_Form):

    """c is the center of the ellipse, rx is the length of the horizontal radius,
    ry is the length of the vertical radius
    """
    def __init__(self, c, rx, ry ,  color=black, identifier=0):
        if not isinstance(c, Point):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(rx, int):
            raise TypeError("The second parameter has to be an integer")
        if not isinstance(ry, int):
            raise TypeError("The second parameter has to be an integer")
        if not isinstance(color, Color):
            raise TypeError("The third parameter has to be a color")
        self.c = c
        self.rx = rx
        self.ry = ry
        self.color = color
        self.identifier = identifier

    def __repr__(self):
        return """Ellipse of center {}, of horizontal radius: {} , of vertical radius: {} and of color: {}
        and of id: {}""".format(self.c, self.rx,self.ry, self.color, self.identifier)

    def get_string(self):

        # method to transform circle into string
        # Ex: Ellipse of center (17,5) and of horizontal axis 7 and of vertical axis 3 => string = "S17,5,7,3"

        string = "E" + str(self.c.x) + "," + str(self.c.y)
        string += "," + str(self.rx) + "," + str(self.ry) + ","
        string += str(self.identifier)
        return string

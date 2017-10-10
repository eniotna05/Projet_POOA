
absciss_max = 10000
ordinate_max = 10000



class Color:

    def __init__(self, R, G, B):

        
        if (not isinstance(R, int) ) or (not isinstance(G, int) ) or (not isinstance(B, int) ):
            raise TypeError("All parameters have to be interger")
        if R < 0 or R > 255 or G < 0 or G > 255 or B < 0 or B > 255:
            raise ValueError("All parameters have to be between 0 and 255")
  
        self.R = R
        self.G = G
        self.B = B
        
    def __repr__(self):
        
        return """Color of RGB code: {}.{}.{}""".format(self.R, self.G, self.B)


white = Color(255,255,255)

black = Color(0,0,0)

class Point:

    def __init__(self, absciss, ordinate):

        global absciss_max
        global ordinate_max
        
        if not isinstance(absciss, int):
            raise TypeError("THe first parameter has to be an integer")
        if not isinstance(ordinate, int):
            raise TypeError("Le second parameter has to be an integer")
        if absciss > absciss_max:
            raise ValueError("The absciss is too high")
        if absciss < 0:
            raise ValueError("THe absciss has to be positive")
        if ordinate > ordinate_max:
            raise ValueError("The ordinate is too high")
        if ordinate < 0:
            raise ValueError("The ordinate has to be positive")


        self.absciss = absciss
        self.ordinate = ordinate
        
    def __repr__(self):
        
        return """Point of absciss {} and ordinate {}""".format(self.abscisse, self.ordonne)  



class Ligne:
    def __init__(self, x, y,color = black):
        if not isinstance(x, Point):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(y, Point):
            raise TypeError("The second parameter has to be a point")
        if not isinstance(color, Color):
            raise TypeError("The third parameter has to be a color")
        self.x = x
        self.y = y
        self.color = color

    def __repr__(self):
        
        return """Ligne from {} to {} and of color: {}""".format(self.x, self.y, self.color)

    def get_string(self):

    # method to transform lign into string
    # Ex: lign from (2,4) to (8,14) => string = "L2,4,8,14"


        string = "L"
        string += str (self.x.absciss)
        string += ","
        string += str (self.x.ordinate)
        string += ","
        string += str (self.y.absciss)
        string += ","
        string += str (self.y.ordinate)
        return string


class Rectangle:
    def __init__(self, x, y,color = black):
        if not isinstance(x, Point):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(y, Point):
            raise TypeError("The second parameter has to be a point")
        if not isinstance(color, Color):
            raise TypeError("The third parameter has to be a color")
        self.x = x
        self.y = y
        self.color = color

    def __repr__(self):
        
        return """Rectangle from {} to {} and of color: {}""".format(self.x, self.y, self.color)

    def get_string(self):

    # method to transform rectangle into string
    # Ex: rectangle from (2,4) to (8,14) => string = "R2,4,8,14"


        string = "R"
        string += str (self.x.absciss)
        string += ","
        string += str (self.x.ordinate)
        string += ","
        string += str (self.y.absciss)
        string += ","
        string += str (self.y.ordinate)
        return string


class Square:
    def __init__(self, x, d ,color = black):
        if not isinstance(x, Point):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(d, int):
            raise TypeError("The second parameter has to be an integer")
        if not isinstance(color, Color):
            raise TypeError("The third parameter has to be a color")
        self.d = d
        self.y = y
        self.color = color

    def __repr__(self):
        
        return """Square of left upper corner: {}, of side length; {} and of color: {}""".format(self.x, self.d, self.color)

    def get_string(self):

    # method to transform square into string
    # Ex: rectangle of left upper corner (17,5) and of side length 2 => string = "S17,5,2"


        string = "S"
        string += str (self.x.absciss)
        string += ","
        string += str (self.x.ordinate)
        string += ","
        string += str (self.d)
        return string


class Circle:
    def __init__(self, c, r,color = black):
        if not isinstance(c, Point):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(r, int):
            raise TypeError("The second parameter has to be an integer")
        if not isinstance(color, Color):
            raise TypeError("The third parameter has to be a color")
        self.r = r
        self.y = y
        self.color = color

    def __repr__(self):
        
        return """Circle of center {}, of radius: {} and of color: {}""".format(self.c, self.r, self.color)

    def get_string(self):

    # method to transform circle into string
    # Ex: Circle of center (17,5) and of radius 2 => string = "S17,5,2"


        string = "C"
        string += str (self.c.absciss)
        string += ","
        string += str (self.c.ordinate)
        string += ","
        string += str (self.r)
        return string







        









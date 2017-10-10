
abscisse_max = 10000
ordonne_max = 10000



class Color:

    def __init__(self, R, G, B):

        
        if (not isinstance(R, int) ) or (not isinstance(G, int) ) or (not isinstance(B, int) ):
            raise TypeError("Tous les parametres doivent etre des entiers")
        if R < 0 or R > 255 or G < 0 or G > 255 or B < 0 or B > 255:
            raise ValueError("Tous les parametres doivent etre entre 0 et 255")
  
        self.R = R
        self.G = G
        self.B = B
        
    def __repr__(self):
        
        return """Couleur de code RGB: {}.{}.{}""".format(self.R, self.G, self.B)


white = Color(255,255,255)

black = Color(0,0,0)

class Point:

    def __init__(self, abscisse, ordonne):

        global abscisse_max
        global ordonne_max
        
        if not isinstance(abscisse, int):
            raise TypeError("Le premier parametre doit être un integer")
        if not isinstance(ordonne, int):
            raise TypeError("Le deuxieme parametre doit être un integer")
        if abscisse > abscisse_max:
            raise ValueError("L'abscisse est trop eleve")
        if abscisse < 0:
            raise ValueError("L'abscisse doit etre positive")
        if ordonne > ordonne_max:
            raise ValueError("L'abscisse est trop eleve")
        if ordonne < 0:
            raise ValueError("L'ordonne doit etre positive")


        self.abscisse = abscisse
        self.ordonne = ordonne
        
    def __repr__(self):
        
        return """Point d"abscisse {} et d'ordonne {}""".format(self.abscisse, self.ordonne)  





class Ligne:
    def __init__(self, point_1, point_2,color = black):
         if not isinstance(point_1, Point):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(point_2, Point):
            raise TypeError("The second parameter has to be a point")
        if not isinstance(color, Color):
            raise TypeError("The third parameter has to be a color")
        self.point_1 = point_1
        self.point_2 = point_2
        self.color = color

    def __repr__(self):
        
        return """Ligne from {} to {} and of color: {}""".format(self.point_1, self.point_2, self.color)

    def get_string(self):

    # method to transform lign into string
    # Ex: lign from (2,4) to (8,14) => string = "L2,4,8,14"


        string = "L"
        string += str (self.point_1.abscisse)
        string += ","
        string += str (self.point_1.ordonne)
        string += ","
        string += str (self.point_2.abscisse)
        string += ","
        string += str (self.point_2.ordonne)
        return string


class Rectangle:
    def __init__(self, point_LU, point_RL, color = black):
        if not isinstance(point_LU, Point):
            raise TypeError("The first parameter has to be a point")
        if not isinstance(point_RL, Point):
            raise TypeError("The second parameter has to be a point")
        if not isinstance(color, Color):
            raise TypeError("The third parameter has to be a color")
        self.point_LU = point_LU
        self.point_RL = point_RL
        self.point_LL = Point(point_LU.abscisse, point_RL.ordonne)
        self.point_RU = Point(point_RL.abscisse, point_LU.ordonne)

        
        self.color = color

    def __repr__(self):
        
        return """Rectrange of left upper corner: {} and of right lower corner: {}""".format(self.point_LU, self.point_RL, self.color)

    def get_string(self):

    # method to transform rectangle into string
    # Ex: rectangle of left upper corner (2,4) and of right lower corner (8,14) => string = "R2,4,8,14"


        string = "R"
        string += str (self.point_LU.abscisse)
        string += ","
        string += str (self.point_LU.ordonne)
        string += ","
        string += str (self.point_RL.abscisse)
        string += ","
        string += str (self.point_RL.ordonne)
        return string



        









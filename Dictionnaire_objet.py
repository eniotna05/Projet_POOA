
abscisse_max = 10000
ordonne_max = 10000

Alphabet =
{1:A
 2:






    }



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
    def __init__(self, point_A, point_B,color = black):
        if not isinstance(point_A, Point):
            raise TypeError("Le premier parametre doit être un point")
        if not isinstance(point_B, Point):
            raise TypeError("Le deuxieme parametre doit être un point")
        if not isinstance(color, Color):
            raise TypeError("Le troisieme parametre doit être une couleur")
        self.point_A = point_A
        self.point_B = point_B
        self.color = color

    def __repr__(self):
        
        return """Ligne entre le {} et le {} de couleur {}""".format(self.point_A, self.point_B, self.color)


class Polygone:
    
    def __init__(self, point_A, point_B, point_C, *points_supplementaires, color = black):

        if (not isinstance(point_A, Point)) or (not isinstance(point_B, Point)) or (not isinstance(point_C, Point)):
            raise TypeError("Tous les parametres doivent etre des points")
        for k in points_supplentaires:
            if not isinstance(k, Point):
                raise TypeError("Tous les parametres doivent etre des points")
        if not isinstance(color, Color):
            raise TypeError("Le parametre couleur doit être une couleur")
        
        self.point_A = point_A
        self.point_B = point_B
        self.point_C = point_C
        for k in point_supplementaires:
            self.point 
            
        self.color = color
        

    def __repr__(self):
        
        return """Polygone de point""".format(self.point_A, self.point_B)








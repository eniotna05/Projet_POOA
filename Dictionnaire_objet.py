
abscisse_max = 10000
ordonne_max = 10000


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
    def __init__(self, point_A, point_B):
        if not isinstance(point_A, Point):
            raise TypeError("Le premier parametre doit être un point")
        if not isinstance(point_B, Point):
            raise TypeError("Le deuxieme parametre doit être un point")
        self.point_A = point_A
        self.point_B = point_B

    def __repr__(self):
        
            return """Ligne entre le {} et le {}""".format(self.point_A, self.point_B)



class Polygone:
    def __init__(self, point_A, point_B, point_C, point_supplementaire*):
        if not isinstance(point_A, Point):
            raise TypeError("Le premier parametre doit être un point")
        if not isinstance(point_B, Point):
            raise TypeError("Le deuxieme parametre doit être un point")
        self.point_A = point_A
        self.point_B = point_B

    def __repr__(self):
        
            return """Ligne entre le {} et le {}""".format(self.point_A, self.point_B)  


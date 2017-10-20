import exchange
from string_to_class import *
from Form_class import *
from Command_class import *


class Stock:

    def __init__(self,identifiant):
        self.identifiant = identifiant
        #dictionnary with the identifier of the form as key, and the form
        self.stock = {}

    def insertForm(self,identifier,form):
        self.stock[identifier] = form
        return self.stock[identifier]

    def __getitem__(self, identifier):
        return self.stock.get(identifier)

    def __iter__(self):
        return iter(self.stock)

    def convertStrIntoForm(self,string):
        #converts an input into the right Form object
        letter = string[0]
        if letter == "R":
            return string_to_rectangle(string[1:])
        elif letter == "C":
            return string_to_circle(string[1:])
        elif letter == "L":
            return string_to_lign(string[1:])
        elif letter == "S":
            return string_to_square(string[1:])

    def _getForm(self,identifier):
        return self.stock[identifier]

    def deleteForm(self,identifier):
        del self.stock[identifier]
        return "The object number {} has been deleted".format(identifier)

    def newObject(self,string):
        parametres = string.split(",")
        identifiant = parametres[-1]
        objet = self.convertStrIntoForm(string)
        self.insertForm(identifiant,objet)
        return self.stock

    def returnStock(self,identifiant):
        return self.stock


if __name__=="__main__":

    Creation_1 = Create(Rectangle(Point(1, 3), Point(10, 100),black,2))
    Creation_2 = Create(Lign(Point(134, 27), Point(1439, 238)))
    Creation_3 = Create(Circle(Point(43, 372), 37))

    string_1 = Creation_1.get_string()
    string_2 = Creation_2.get_string()
    string_3 = Creation_3.get_string()

    print(string_1)

    essai = Stock("anais")
    essai.newObject(string_1)
    essai.newObject(string_2)
    print(essai.stock)
    for element in essai.stock:
        print(essai.stock[element])

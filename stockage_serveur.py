import exchange
from string_to_class import *
from Form_class import *
from Command_class import *


class Stock:

    def __init__(self, username):
        self.username = username
        # Dict with the identifier of the form as key, and the form
        self.stock = {}
        self.form_pile = []

    def newObject(self, string):
        parameter = string.split(",")
        identifier = parameter[-1]
        form = string_to_command(string).created_form
        self.insertForm(identifier, form)
        print(self.stock)
        print(self.form_pile)
        return self.stock

    def insertForm(self, identifier, form):
        self.stock[identifier] = form
        self.form_pile.insert(0, identifier)
        return self.stock[identifier]

    def __getitem__(self, identifier):
        return self.stock.get(identifier)

    def __iter__(self):
        return iter(self.stock)

    def __delitem__(self, key):
        del self.stock[key]


    def _getForm(self, identifier):
        return self.stock[identifier]

    def deleteForm(self, identifier):
        del self.stock[identifier]
        self.form_pile.remove(identifier)
        print("The object number {} has been deleted".format(identifier))
        print(self.stock)
        print(self.form_pile)


    def convertStockIntoStr(self):
        #TODO : Check that this sends forms in the right order
        """Transforms all the form data stocked in the server into a string
        for sending to new clients
        """
        concatenate_elements = ""
        for id in self.form_pile:
            string = self.stock[id].get_string()
            concatenate_elements += string + "."
        return concatenate_elements[:-1]


if __name__ == "__main__":

    Creation_1 = Create(WB_Rectangle(Point(1, 3), Point(10, 100), black, 2))
    Creation_2 = Create(WB_Line(Point(134, 27), Point(1439, 238), black, 30))
    Creation_3 = Create(WB_Circle(Point(43, 372), 37))

    string_1 = Creation_1.get_string()
    string_2 = Creation_2.get_string()
    string_3 = Creation_3.get_string()

    essai = Stock("anais")
    essai.newObject(string_1)
    essai.newObject(string_2)
    essai.newObject(string_3)
    print(essai.stock)
    print(essai.convertStockIntoStr())
    essai.deleteForm("30")
    print(essai.convertStockIntoStr())


#TODO: Supprimer ce fichier une fois que Server_Database est opérationel

from utils.string_to_class import string_to_command


class Stock:

    def __init__(self, username):
        self.username = username
        # Dict with the identifier of the form as key, and the form
        self.stock = {}
        self.form_pile = []

    def new_object(self, string):
        parameter = string.split(",")
        identifier = parameter[-1]
        form = string_to_command(string).created_form
        self._insert_form(identifier, form)

        return self.stock

    def _insert_form(self, identifier, form):
        self.stock[identifier] = form
        self.form_pile.insert(0, identifier)
        return self.stock[identifier]

    def __getitem__(self, identifier):
        return self.stock.get(identifier)

    def __iter__(self):
        return iter(self.stock)

    def __delitem__(self, key):
        del self.stock[key]

    def _get_form(self, identifier):
        return self.stock[identifier]

    def delete_form(self, identifier):
        del self.stock[identifier]
        self.form_pile.remove(identifier)


    def convert_stock_into_str(self):
        # TODO : Check that this sends forms in the right order
        """Transforms all the form data stocked in the server into a string
        for sending to new clients
        """
        concatenate_elements = ""
        for id in self.form_pile:
            string = self.stock[id].get_string()
            concatenate_elements += string + "."
        return concatenate_elements[:-1]


# if __name__ == "__main__":
#
#     Creation_1 = Create(WBRectangle(WBPoint(1, 3), Point(10, 100), black, 2))
#     Creation_2 = Create(WBLine(WBPoint(134, 27), Point(1439, 238), black, 30))
#     Creation_3 = Create(WBCircle(WBPoint(43, 372), 37))
#
#     string_1 = Creation_1.get_string()
#     string_2 = Creation_2.get_string()
#     string_3 = Creation_3.get_string()
#
#     essai = Stock("anais")
#     essai.new_object(string_1)
#     essai.new_object(string_2)
#     essai.new_object(string_3)
#     print(essai.stock)
#     print(essai.convert_stock_into_str())
#     essai.delete_form("30")
#     print(essai.convert_stock_into_str())

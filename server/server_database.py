from utils.string_to_class import string_to_command



class ServerDatabase:
    """This class stores a dictionnary and a pile of the forms created by
    clients
    Its purpose is to allow new clients connecting to an ongoing session to
    receive the forms that were created before they connected """
    def __init__(self):
        # Dict with the identifier of the form as key, and the form
        self.stock = {}
        self.form_pile = []

    def new_object(self, string):
        parameter = string.split(",")
        identifier = parameter[-1]
        form = string_to_command(string).created_form
        self.stock[identifier] = form
        self.form_pile.insert(0, identifier)
        print("The object number {} has been created".format(identifier))
        # TODO : Supprime ces prints
        print(self.stock)
        print(self.form_pile)
        return self.stock

    def _get_form(self, identifier):
        return self.stock[identifier]

    def delete_form(self, identifier):
        del self.stock[identifier]
        self.form_pile.remove(identifier)
        print("The object number {} has been deleted".format(identifier))
        # TODO : Supprime ces prints
        print(self.stock)
        print(self.form_pile)

    def convert_database_into_str(self):
        """Transforms all the form data stocked in the server into a string
        for sending to new clients
        """
        concatenate_elements = ""
        for id in self.form_pile:
            string = self.stock[id].get_string()
            concatenate_elements = string + "." + concatenate_elements
        return concatenate_elements[:-1]




    # TODO: verifier utilité de ces trois fonctions
    def __getitem__(self, identifier):
        return self.stock.get(identifier)

    def __iter__(self):
        return iter(self.stock)

    def __delitem__(self, key):
        del self.stock[key]
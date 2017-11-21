# File defining the data structure that the server uses to keep an history of
# the forms that were created by the users.

from utils.string_to_class import string_to_command


class ServerDatabase:
    """This class stores a dictionnary and a pile of the forms created by
    clients.
    Its purpose is to allow new clients connecting to an ongoing session to
    receive the forms that were created before they connected """

    def __init__(self):
        # Dict with the identifier of the form as key, and the form
        self.stock = {}
        self.form_pile = []
        # list of socker connexions with clients
        self.connexions = []

    def create_object(self, string):
        """Add a new object to the history"""
        parameter = string.split(",")
        identifier = parameter[-1]
        form = string_to_command(string).created_form
        self.stock[identifier] = form
        self.form_pile.insert(0, identifier)
        print("The object number {} has been created".format(identifier))
        return self.stock

    def delete_form(self, identifier):
        """Remove an object from the history"""
        del self.stock[identifier]
        self.form_pile.remove(identifier)
        print("The object number {} has been deleted".format(identifier))

    def convert_database_into_str(self):
        """Transforms all the form data stocked in the server into a string
        to send it to new clients"""
        concatenate_elements = ""
        for id in self.form_pile:
            string = self.stock[id].get_string()
            concatenate_elements = string + "." + concatenate_elements
        return concatenate_elements[:-1]

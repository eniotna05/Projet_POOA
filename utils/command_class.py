# This file defines different classes that correspond to different commands
# that can be executed on the client


class Create:
    """Command to create an item"""

    def __init__(self, created_form):
        self.created_form = created_form

    def __repr__(self):
        return """Creation of the form: {}""".format(self.created_form)

    def get_string(self):
        """method to transform command into string
        return string of created form"""
        return self.created_form.get_string()


class DeleteRequest:
    """Class to ask permission to delete an item that is not yours"""

    def __init__(self, form_id, requester):
        """form_id is like antoine3, requester is like yoann"""
        if not isinstance(form_id, str):
            raise TypeError("The parameter has to be a string")
        self._form_id = form_id
        self._symbol = "Z"
        self._requester = requester

    def __repr__(self):
        return """Demend of deletion of the form id: {}
        requested by {} """.format(self.form_id, self.requester)

    def get_string(self):
        """method to transform command into string
        Ex: ask of deletion of Form 45, owned by antoine, request emmited by yoann
        => return Zantoine45,yoann"""
        return self._symbol + self._form_id + "," + self._requester

    @property
    def form_id(self):
        return self._form_id

    @property
    def requester(self):
        return self._requester


class Delete:
    """Class defining an order to remove an item from connected clients"""

    def __init__(self, form_id):
        """form_id is like antoine3"""
        if not isinstance(form_id, str):
            raise TypeError("The parameter has to be a string")
        self._form_id = form_id
        self._symbol = "D"

    def __repr__(self):
        return """Deletion of the form id:{} """.format(self.form_id)

    def get_string(self):
        """method to transform command into string
        Ex: deletion of Form 45, owned by antoine
        => return Dantoine45"""
        return self._symbol + self._form_id

    @property
    def form_id(self):
        return self._form_id


class NegativeAnswer:
    """Class to inform another client that his deletion demend is refused"""

    def __init__(self, form_id, receptor):
        """form_id is the id of the form concerned like antoine3,
        receptor is the client that made the demend like yoann"""
        if not isinstance(form_id, str):
            raise TypeError("The parameter has to be a string")
        self._form_id = form_id
        self._receptor = _receptor
        self._symbol = "N"

    def __repr__(self):
        return """Refusal to delete message of form
        of form id:{} to receptor:{} """.format(self._form_id, self._receptor)

    def get_string(self):
        """method to transform command into string
        Ex: negative answer of Form 45, owned by antoine to yoann
        => return Aantoine45,yoann"""
        return self._symbol + self._form_id + "," + self._receptor

    @property
    def form_id(self):
        return self._form_id


class Quit:

    def __init__(self):
        self.symbol = "Q"
        self.message = "You are disconnected from the server"

    def get_string(self):
        return self.symbol


class Hello:

    def __init__(self):
        self.symbol = "H"
        self.message = "The client is connected to the server"

    def get_string(self):
        return self.symbol


# Ununsed for now
class Move:
    """ horizontal movement and y = vertical movement
    x an y are integers and can be negative """

    def __init__(self, form_id, x, y):
        if not isinstance(form_id, str):
            raise TypeError("The parameter has to be a string")
        if not isinstance(x, int):
            raise TypeError("The parameter has to be a string")
        if not isinstance(y, int):
            raise TypeError("The parameter has to be a string")

        self._form_id = form_id
        self._x = x
        self._y = y
        self._symbol = "M"

    def __repr__(self):
        return """Moving of the form: {}, horizontal movement = {},
        vertical movement = {}""".format(self._form_id, self._x, self._y)

    def get_string(self):
        """method to transform command into string
        return string of created form"""
        return self._symbol + self._form_id + "," \
            + str(self._x) + "," + str(self._y)

    @property
    def form_id(self):
        return self._form_id

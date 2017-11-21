# This file defines different classes that correspond to different commands
# that are sent by clients to other clients through the server. They are
# converted to string form when sent


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
        Ex: ask of deletion of Form 45, owned by antoine, request emmited by
        yoann => return Zantoine45,yoann"""
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
        self._receptor = receptor
        self._symbol = "N"

    def __repr__(self):
        return """Refusal to delete message of form
        of form id:{} to receptor:{} """.format(self._form_id, self._receptor)

    def get_string(self):
        """method to transform command into string
        Ex: negative answer of Form 45, owned by antoine to yoann
        => return Nantoine45,yoann"""
        return self._symbol + self._form_id + "," + self._receptor

    @property
    def form_id(self):
        return self._form_id

    @property
    def receptor(self):
        return self._receptor


class Quit:
    """Class to inform client that he is disconnected"""
    def __init__(self):
        self.symbol = "Q"
        self.message = "You are disconnected from the server"

    def get_string(self):
        return self.symbol


class Hello:
    """Class to inform client that he is connected"""
    def __init__(self):
        self.symbol = "H"
        self.message = "The client is connected to the server"

    def get_string(self):
        return self.symbol




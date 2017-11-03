class Create:

    def __init__(self, created_form):
        self.created_form = created_form

    def __repr__(self):
        return """Creation of the form: {}""".format(self.created_form)

    def get_string(self):
        """method to transform command into string
        return string of created form"""
        return self.created_form.get_string()


class Delete:

    def __init__(self, form_id, requester):
        """form_id is like antoine3, requester is like yoann"""
        if not isinstance(form_id, str):
            raise TypeError("The parameter has to be a string")
        self._form_id = form_id
        self._symbol = "D"
        self._requester = requester

    def __repr__(self):
        return """Deletion of the form id: """.format(self.form)

    def get_string(self):
        """method to transform command into string
        Ex: deletion of Form 45, owned by antoine, request emmited by yoann
        => return Dantoine45,yoann"""
        return self._symbol + self._form_id + "," + self._requester

    @property
    def form_id(self):
        return self._form_id

    @property
    def requester(self):
        return self._requester


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

        self.form_id = form_id
        self.x = x
        self. y = y
        self.symbol = "M"

    def __repr__(self):
        return """Moving of the form: {}, horizontal movement = {},
        vertical movement = {}""".format(self.form_id, self.x, self. y)

    def get_string(self):
        """method to transform command into string
        return string of created form"""
        return self.symbol + self.form_id + ","
        + str(self.x) + "," + str(self.y)

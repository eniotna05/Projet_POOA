from utils.command_class import Delete


class SessionManager():
    """This class is used to exchange data between the network-related thread
    client and the kivy objects like whiteboard and toolbar.
    It stores the forms both in a dictionnary (for keeping id and references of
    objects drawn on the board's canvas) and in a pile (for keeping a track of
    the order of form adding to undo recent changes and know which one is on
    top) and update them simultaneously"""

    def __init__(self, sending_queue):
        self._client_id = None
        self._is_connected = False
        self.local_database = {}
        self.form_pile = []
        self._form_number = 0
        self.sending_queue = sending_queue

    @property
    def form_number(self):
        return self._form_number

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, client_id=None):
        self._client_id = client_id

    @property
    def is_connected(self):
        return self._is_connected

    @is_connected.setter
    def is_connected(self, is_connected=False):
        self._is_connected = is_connected

    def store_internal_form(self, form):
        """Saving an internally created object to a local dictionnary for future
        reference and putting it into the sending queue (for the network thread
        to send it)"""
        self._form_number += 1
        if self._is_connected:
            form_id = self._client_id + "-" + str(self._form_number)
        else:
            form_id = str(self._form_number)
        form.identifier = form_id
        self.local_database[form_id] = form
        self.form_pile.insert(0, form.identifier)

        self.sending_queue.put(form.get_string())

        return form_id

    def store_external_form(self, form):
        """Saving a received object to a local dictionnary for future reference
        """

        self.local_database[form.identifier] = form
        self.form_pile.insert(0, form.identifier)

        return form.identifier

    def delete_form(self, form_id, send_to_server=False):
        """Delete a form from the local database. If send_to_server is True, a
        request to delete this form will be sent to the server"""

        if send_to_server:
            self.sending_queue.put(Delete(form_id).get_string())
        self.form_pile.remove(form_id)
        del self.local_database[form_id]

    def extract_top_form(self, x, y):
        """Gets the top form on the board in (x,y) coordinates"""
        for k in self.form_pile:
            if self.local_database[k].check_inclusion(x,y)== True:
                return self.local_database[k]
        return None

    def extract_last_created(self):
        """Gets the last created form on the board in (x,y) coordinates"""
        for k in self.form_pile:
            if k.split("-")[0] == self.client_id:
                return k
        return None

class SessionManager():

    """This class is used to exchange data between the network-related thread
    client and the kivy objects like whiteboard and toolbar
    """

    def __init__(self, sending_queue):
        self._client_id = None
        self._connected = False
        self.local_database = {}
        self._form_number = 0
        self.sending_queue = sending_queue

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, client_id=None):
        self._client_id = client_id

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, connected=False):
        self._connected = connected

    def store_form(self, form):
        """Saving an object to a local dictionnary for future reference and
        putting it into the sending queue (for the network thread to send it)
        """
        self._form_number += 1
        form_id = self._client_id + str(self._form_number)
        form.identifier = form_id
        self.local_database[form_id] = form
        self.sending_queue.put(form.get_string())

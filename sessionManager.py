from Command_class import Delete, Delete_demend


class SessionManager():

    """This class is used to exchange data between the network-related thread
    client and the kivy objects like whiteboard and toolbar
    """

    def __init__(self, sending_queue):
        self._client_id = None
        self._is_connected = False
        self.local_database = {}
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
        reference and putting it into the sending queue
        (for the network thread to send it)
        """
        self._form_number += 1
        if self._is_connected:
            form_id = self._client_id + str(self._form_number)
        else:
            form_id = str(self._form_number)
        form.identifier = form_id
        self.local_database[form_id] = form
        self.sending_queue.put(form.get_string())
        return form_id

    def store_external_form(self, form):
        """Saving a received object to a local dictionnary for future reference
        """

        self.local_database[form.identifier] = form

        return form.identifier

    def delete_form(self, form_id, source):
        """Delete a form from the local database.
         Source is either "ext", you received an order to delete from the server
         or "int" if
         If source is "int", order to delete will also be sent to server
         so that other client can delete it
         """
        if source == "int":
            self.sending_queue.put(Delete(form_id).get_string())

        del self.local_database[form_id]



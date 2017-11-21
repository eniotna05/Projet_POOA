from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class WB_Popup(Popup):
    """Generic & custom class defining a Popup"""

    def __init__(self, title="", text_content=""):
        Popup.__init__(self, title=title)
        # kivy properties defining the popup
        self.content = BoxLayout(orientation='vertical')
        self.auto_dismiss = False
        self.size_hint = (0.5, 0.5)
        self.size = (300, 300)

        self.content.add_widget(Label(text=text_content))

    def close(self, instance):
        self.dismiss()


class Error_Popup(WB_Popup):
    """Popup showing an error message to the user and a "OK" button"""

    def __init__(self, text_content="Unknown Error !"):
        WB_Popup.__init__(self, title="Error", text_content=text_content)
        self._button = Button(text="Ok")
        self._button.bind(on_release=self.close)
        self.content.add_widget(self._button)


class Input_Popup(WB_Popup):
    """Popup asking for some text user input, with a "OK" button. The text that
    the user typed in is stored in the public variable "return_value for later
    reuse"""

    def __init__(self, title="", text_content="", hint_text="", error_popup=None):
        WB_Popup.__init__(self, title=title, text_content=text_content)
        self._error_popup = error_popup
        self._return_value = ""

        self._text_input = TextInput(multiline=False, hint_text=hint_text)
        self._text_input.bind(on_text_validate=self.on_enter)
        self.content.add_widget(self._text_input)

        self._button = Button(text="Ok")
        self._button.bind(on_release=self.on_validate)
        self.content.add_widget(self._button)

    def on_enter(self, instance):

        if instance.text == "":
            if self._error_popup is not None:
                self._error_popup.open()
        else:
            self._return_value = instance.text
            self.dismiss()

    def on_validate(self, instance):
        if self._text_input.text == "":
            if self._error_popup is not None:
                self._error_popup.open()
        else:
            self._return_value = self._text_input.text
            self.dismiss()

    @property
    def return_value(self):
        return self._return_value


class Initial_Popup(Input_Popup):
    """Special Input_Popup, showing two text input boxes instead of one. The
    second text input is asking for an IP address, and that address is stored
    in the public "ip_value" variable"""

    def __init__(self, title="", text_content="", hint_text="", hint_IP="",
                 error_popup=None):
        Input_Popup.__init__(self, title=title, text_content=text_content,
                             hint_text=hint_text, error_popup=error_popup)
        self._ip_value = ""

        self._ip_input = TextInput(multiline=False, hint_text=hint_IP)
        self._ip_input.bind(on_text_validate=self.on_enter)
        self.content.add_widget(self._ip_input, 1)

    # override the super class method, preventing direct validation
    def on_enter(self, instance):
        pass

    def on_validate(self, instance):
        if self._text_input.text == "" or self._ip_input.text == "":
            if self._error_popup is not None:
                self._error_popup.open()
        else:
            self._return_value = self._text_input.text
            self._ip_value = self._ip_input.text
            self.dismiss()

    @property
    def ip_value(self):
        return self._ip_value


class Question_Popup(WB_Popup):
    """Popup asking a question to the user qith a yes/no answer. The result is
    stored as a string "yes" or "no" in the public variable "return_value"."""

    def __init__(self, title="", question=""):
        WB_Popup.__init__(self, title=title, text_content=question)
        self._return_value = ""

        self._yes_button = Button(text="yes")
        self._yes_button.bind(on_release=self.on_yes_answer)
        self.content.add_widget(self._yes_button)

        self._no_button = Button(text="no")
        self._no_button.bind(on_release=self.on_no_answer)
        self.content.add_widget(self._no_button)

    def on_yes_answer(self, instance):
        self._return_value = instance.text
        self.dismiss()

    def on_no_answer(self, instance):
        self._return_value = instance.text
        self.dismiss()

    @property
    def return_value(self):
        return self._return_value

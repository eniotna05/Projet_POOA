import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class WB_Popup(Popup):

    def __init__(self):
        Popup.__init__(self)
        self.title=""
        self.auto_dismiss = False
        self.size_hint = (0.5, 0.5)
        self.size = (300, 300)
        self.content = Popup_Content("", "")
        self.content.button.bind(on_release=self._on_answer)

    def _on_answer(self):
        pass


class Popup_Content(BoxLayout):

    def __init__(self, text_content, text_close_button, text_window=False):
        super().__init__(orientation='vertical')
        self.text_content = text_content
        self.text_close_button = text_close_button
        self.text_window = text_window
        self.text_input = "John Doe"
        self.label = Label(text=self.text_content)
        self.button = Button(text=self.text_close_button)
        self.case_text_input = TextInput(text=self.text_input)
        self.add_widget(self.label)
        self.output = Label(text="John Doe")
        if self.text_window:
            self.add_widget(self.case_text_input)
            self.case_text_input.bind(text=self.get_user_text)
        self.add_widget(self.button)

    def get_user_text(self, instance, value):
        self.output.text = value
        print(self.output.text)
        return self.output.text


class Start_Popup(WB_Popup):

    def __init__(self):
        WB_Popup.__init__(self)
        self.popup_content = Popup_Content("Please enter your username", "Enter",text_window=True)
        self.content = self.popup_content
        self.content.button.bind(on_release=self.close)

    def close(self,value):
        if self.popup_content.output.text == "John Doe":
            error_popup = Error_Popup()
            error_popup.open()
        else:
            self.dismiss()


class Error_Popup(WB_Popup):
    def __init__(self):
        WB_Popup.__init__(self)
        self.popup_content = Popup_Content("You have not entered your username !",
                                            "Ok",text_window=False)
        self.content = self.popup_content
        self.content.button.bind(on_release=self.close)

    def close(self,value):
        self.dismiss()

class Delete_Popup(WB_Popup):

    def __init__(self, requester, form):
        self.requester = requester
        self.form = form
        WB_Popup.__init__(self)
        self.popup_content = Popup_Content(self.requester + " wishes to delete one of\n"
                                                            "the form that you created: \n"
                                                            + self.form +
                                                            "\nPress Ok to accept and No to refuse",
                                           "Ok")
        self.popup_content.add_widget(Button(text="Nope"))
        self.content = self.popup_content



class MyApp(App):

    def build(self):
        self.popup = Delete_Popup("antoine","fewr")
        self.popup.open()



if __name__ == "__main__":
    MyApp().run()

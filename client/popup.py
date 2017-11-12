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
        self.content = Popup_Content("")


class Popup_Content(BoxLayout):

    def __init__(self, text_content):
        super().__init__(orientation='vertical')
        self.text_content = text_content
        self.label = Label(text=self.text_content)
        self.add_widget(self.label)


class Start_Popup(WB_Popup):

    def __init__(self):
        WB_Popup.__init__(self)
        self.popup_content = Popup_Content("Please enter your username")
        self.content = self.popup_content
        self.text_input = TextInput(multiline=False)
        self.text_input.bind(on_text_validate=self.on_enter)
        self.popup_content.add_widget(self.text_input)
        self.username = ""

    def on_enter(self, instance):
        self.username = self.text_input.text
        if self.username == "":
            error_popup = Error_Popup()
            error_popup.open()
        else:
            self.dismiss()
            return self.text_input.text


class Error_Popup(WB_Popup):
    def __init__(self):
        WB_Popup.__init__(self)
        self.popup_content = Popup_Content("You have not entered your username !")
        self.content = self.popup_content
        self.button = Button(text="Ok")
        self.button.bind(on_release=self.close)
        self.popup_content.add_widget(self.button)

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
        self.popup = Start_Popup()
        self.popup.open()



if __name__ == "__main__":
    MyApp().run()

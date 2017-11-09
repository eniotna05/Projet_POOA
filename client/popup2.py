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

    def __init__(self, title="", text_content=""):
        Popup.__init__(self, title=title)
        self.content = BoxLayout(orientation='vertical')
        self.auto_dismiss = False
        self.size_hint = (0.5, 0.5)
        self.size = (300, 300)

        self.content.add_widget(Label(text=text_content))

    def close(self, instance):
        self.dismiss()


class Error_Popup(WB_Popup):

    def __init__(self, text_content="Unknown Error !"):
        WB_Popup.__init__(self, title="Error", text_content=text_content)
        self.button = Button(text="Ok")
        self.button.bind(on_release=self.close)
        self.content.add_widget(self.button)


class Input_Popup(WB_Popup):

    def __init__(self, title="", text_content="", hint_text="", error_popup=None):
        WB_Popup.__init__(self, title=title, text_content=text_content)
        self.error_popup = error_popup
        self._return_value = ""

        self.text_input = TextInput(multiline=False, hint_text=hint_text)
        self.text_input.bind(on_text_validate=self.on_enter)
        self.content.add_widget(self.text_input)

        self.button = Button(text="Ok")
        self.button.bind(on_release=self.on_validate)
        self.content.add_widget(self.button)

    def on_enter(self, instance):

        if instance.text == "":
            if self.error_popup is not None:
                self.error_popup.open()
        else:
            self._return_value = instance.text
            self.dismiss()

    def on_validate(self, instance):
        if self.text_input.text == "":
            if self.error_popup is not None:
                self.error_popup.open()
        else:
            self._return_value = self.text_input.text
            self.dismiss()

    @property
    def return_value(self):
        return self._return_value

#Delete_Popup  ==> en devoirs ;-P Mais suggestion : faire en sorte que t'aie juste
# besoin de passer des paramètres au constructeur et que ça soit une classe plus
# générique "question/réponse + bouttons oui/non", et on pourra l'utiliser pour
# des tas d'autres trucs


class Question_Popup(WB_Popup):

    def __init__(self, title="", question=""):
        WB_Popup.__init__(self, title=title, text_content=question)
        self._return_value = ""

        self.yes_button = Button(text="yes")
        self.yes_button.bind(on_release=on_yes_answer)
        self.content.add_widget(self.yes_button)

        self.no_button = Button(text="no")
        self.no_button.bind(on_release=on_no_answer)
        self.content.add_widget(self.no_button)

    def on_yes_answer(self, instance):
        self._return_value = instance.text
        self.dismiss()

    def on_no_answer(self, instance):
        self._return_value = instance.text
        self.dismiss()

    @property
    def return_value(self):
        return self._return_value


class MyApp(App):

    def build(self):

        self.popup = Input_Popup(
            title="Welcome",
            text_content="Please enter your username",
            hint_text="John Doe",
            error_popup=Error_Popup(text_content="You have not entered your username !"))
        self.popup.bind(on_dismiss=self.update_username)
        self.popup.open()

        # La même chose pour moi quand j'en ai besoin pour récupérer le texte
        # que l'user veut dessiner
        # self.draw_text_popup = Input_Popup(
        #     title="Draw Text",
        #     text_content="Enter the text you want to write"
        #     error_popup=Error_Popup(text_content="You have not written any text")
        # )
        # self.popup.bind(on_dismiss=self.update_draw_text)
        # self.draw_text_popup.open()

    def update_username(self, instance):
        print(self.popup.return_value)






if __name__ == "__main__":
        MyApp().run()

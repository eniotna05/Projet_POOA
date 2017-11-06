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



class Close_Button(Button):

    def __init__(self):
        Button.__init__(self)

    def close_text(self, close_text):
        self.text = close_text


class ContentPopup(BoxLayout):

    def __init__(self):
        BoxLayout.__init__(self)
        self.close_button = Button(text="close")
        self.add_widget(self.close_button)


class WB_Popup(Popup):

    def __init__(self):
        Popup.__init__(self)
        self.content = ContentPopup()
        self.auto_dismiss = False
        self.size_hint = (None, None)
        self.size = (480, 400)


class MyApp(App):

    def build(self):
        self.popup = WB_Popup()
        self.popup.content.close_button.bind(on_release=self.on_answer)
        self.popup.open()

    def on_answer(self):
        self.popup.dismiss()

if __name__ == "__main__":
    MyApp().run()

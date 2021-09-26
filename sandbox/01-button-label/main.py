from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


class Container(BoxLayout):
    label_text = StringProperty("Click the button and see what happens...")
    def handle_button_click(self):
        print("Button pressed")
        self.label_text = "Wow. You actually did it."


class ButtonLabelApp(App):
    pass

ButtonLabelApp().run()

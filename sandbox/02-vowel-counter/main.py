from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty


class Container(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        title_label = Label(
            pos_hint={"center_y": 0.8},
            size_hint=(1, None),
            font_size="50dp",
            text="Count Vowels"
        )
        self.text_input = TextInput(
            size_hint=(0.75, None),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            font_size="25dp",
            hint_text="Enter some text..."
        )
        self.count_button = Button(
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            size_hint=(0.75, None),
            height="80dp",
            text="Count!",
            on_press=self.handle_button_press
        )
        self.result_label = Label(
            pos_hint={"center_y": 0.2},
            size_hint=(1, None),
            font_size="20dp",
            text="hello"
        )
        self.add_widget(title_label)
        self.add_widget(self.text_input)
        self.add_widget(self.count_button)
        self.add_widget(self.result_label)

    def handle_button_press(self, button: Button):
        text = self.text_input.text.lower()

        count = 0
        for c in text:
            if c in list("aeiou"):
                count += 1
        
        msg = f"There are {count} vowels in the text."
        
        self.result_label.text = msg



class CountVowelApp(App):
    def build(self):
        return Container()

CountVowelApp().run()

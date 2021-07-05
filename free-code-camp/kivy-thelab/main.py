from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Ellipse, Line, Rectangle
from kivy.metrics import dp
from kivy.properties import BooleanProperty, Clock, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget


class WidgetsExample(GridLayout):
    count = 1
    count_enabled = BooleanProperty(False)
    my_text = StringProperty("1")
    text_input_str = StringProperty("foo")
    # slider_value_txt = StringProperty("50")

    def on_button_click(self):
        if self.count_enabled:
            self.count += 1
        self.my_text = str(self.count)
    
    def on_toggle_button_state(self, toggle):
        print(f"State: {toggle.state}")
        if toggle.state == "normal":  # OFF
            toggle.text = "OFF"
            self.count_enabled = False
        else:  # ON
            toggle.text = "ON"
            self.count_enabled = True
    
    def on_switch_active(self, switch):
        print(f"Switch: {switch.active}")
    
    def on_slider_value(self, slider):
        print(f"Slider: {int(slider.value)}" )
        # self.slider_value_txt = str(int(slider.value)
    
    def on_text_validate(self, text_input):
        self.text_input_str = text_input.text


class StackLayoutExample(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "lr-tb"
        for n in range(1, 101):
            b = Button(text=str(n), size_hint=(None, None), size=(dp(100), dp(100)))
            self.add_widget(b)

# class GridLayoutExample(GridLayout):
#     pass


class AnchorLayoutExample(AnchorLayout):
    pass


class BoxLayoutExample(BoxLayout):
    pass


class MainWidget(Widget):
    pass


class TheLabApp(App):
    pass


class CanvasExample1(Widget):
    pass


class CanvasExample2(Widget):
    pass


class CanvasExample3(Widget):
    pass


class CanvasExample4(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Line(points=(100, 100, 400, 500), width=2)
            Color(0, 1, 0)
            Line(circle=(400, 200, 80), width=2)
            Line(rectangle=(200, 300, 150, 100), width = 5)
            self.rect = Rectangle(pos=(400, 200), size=(150, 100))
    
    def on_button_press(self):
        x, y = self.rect.pos
        rect_w, rect_h = self.rect.size
        new_x = min(max(0, x + 10), self.width - rect_w)
        self.rect.pos = new_x, y


class CanvasExample5(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ball_size = dp(50)
        self.dx = dp(3)
        self.dy = dp(3)
        with self.canvas:
            self.ball = Ellipse(pos=(dp(100), dp(100)), size=(self.ball_size, self.ball_size))
        
        Clock.schedule_interval(self.update, 1/60)

    def on_size(self, *args):
        # print(f"on size: {self.width}, {self.height}")
        self.ball.pos = (self.center_x - self.ball_size//2, self.center_y - self.ball_size//2)

    def update(self, dt):
        x, y = self.ball.pos
        x += self.dx
        y += self.dy

        if x > self.width - self.ball_size or x < 0:
            self.dx *= -1
        if y > self.height - self.ball_size or y < 0:
            self.dy *= -1

        self.ball.pos = x, y


class CanvasExample6(Widget):
    pass


class CanvasExample7(BoxLayout):
    pass

TheLabApp().run()

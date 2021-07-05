from kivy.uix.relativelayout import RelativeLayout


def on_keyboard_up(self, keyboard, keycode):
    self.stop()
    return True

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'left':
        self.move_left()
    elif keycode[1] == 'right':
        self.move_right()
    return True

def on_touch_down(self, touch):
    if not self.game_over_state and self.game_has_started:
        if touch.x < self.width//2:
            self.move_left()
        else:
            self.move_right()
    return super(RelativeLayout, self).on_touch_down(touch)

def on_touch_up(self, touch):
    self.stop()

def move_left(self):
    self.current_speed_x = self.SPEED_X

def move_right(self):
    self.current_speed_x = -self.SPEED_X

def stop(self):
    self.current_speed_x = 0

def keyboard_closed(self):
    self.keyboard.unbind(on_key_down=self.on_keyboard_down)
    self.keyboard.unbind(on_key_up=self.on_keyboard_up)
    self.keyboard = None
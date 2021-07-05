import random

from kivy.config import Config
ORIGINAL_WIDTH = 900
ORIGINAL_HEIGHT = 400
Config.set("graphics", "width", str(ORIGINAL_WIDTH))
Config.set("graphics", "height", str(ORIGINAL_HEIGHT))

from kivy.utils import platform
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Quad, Triangle
from kivy.properties import Clock, NumericProperty, ObjectProperty, StringProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from kivy.core.audio import SoundLoader


Builder.load_file("menu.kv")

class MainWidget(RelativeLayout):
    from transforms import transform_2D, transform_perspective, transform
    from user_actions import on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up, keyboard_closed, move_left, move_right, stop

    menu_widget = ObjectProperty()
    menu_label_title = StringProperty("   ".join(list("GALAXY")))
    menu_button_text = StringProperty("START")
    score_text = StringProperty("SCORE: 0")
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 10
    # V_NB_LINES = 4
    V_LINES_SPACING = 0.25  # percent of screen width
    # V_LINES_SPACING = 0.1  # percent of screen width
    vertical_lines = None

    H_NB_LINES = 10
    H_LINES_SPACING = 0.1  # percent of screen width
    horizontal_lines = None

    SPEED = 1
    current_offset_y = 0
    current_y_loop = 0

    SPEED_X = 12
    current_speed_x = 0
    current_offset_x = 0

    tiles = []
    NB_TILES = 16
    tiles_coordinates = []

    SHIP_WIDTH = 0.1
    SHIP_HEIGHT = 0.035
    SHIP_BASE_Y = 0.04
    ship = None
    ship_coordinates = [(0, 0), (0, 0), (0, 0)]

    game_over_state = False
    game_has_started = False

    sound_begin = None
    sound_galaxy = None
    sound_gameover_impact = None
    sound_gameover_voice = None
    sound_music1 = None
    sound_restart = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(f"INIT: {self.width}, {self.height}")
        self.vertical_lines = []
        self.horizontal_lines = []
        self.init_audio()
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_ship()
        self.reset_state()

        if self.is_desktop():
            self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self.keyboard.bind(on_key_down=self.on_keyboard_down)
            self.keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1/60)

        self.sound_galaxy.play()
    
    def init_audio(self):
        self.sound_begin = SoundLoader.load("assets/audio/begin.wav")
        self.sound_galaxy = SoundLoader.load("assets/audio/galaxy.wav")
        self.sound_gameover_impact = SoundLoader.load("assets/audio/gameover_impact.wav")
        self.sound_gameover_voice = SoundLoader.load("assets/audio/gameover_voice.wav")
        self.sound_music1 = SoundLoader.load("assets/audio/music1.wav")
        self.sound_restart = SoundLoader.load("assets/audio/restart.wav")

        self.sound_music1.volume = 1
        self.sound_begin.volume = 0.25
        self.sound_galaxy.volume = 0.25
        self.sound_gameover_impact.volume = 0.6
        self.sound_gameover_voice.volume = 0.25
        self.sound_restart.volume = 0.25

    def reset_state(self):
        self.current_offset_y = 0
        self.current_y_loop = 0
        self.current_speed_x = 0
        self.current_offset_x = 0
        self.tiles_coordinates = []
        self.score_text = "SCORE: 0"
        self.prefill_tiles_coordinates()
        self.generate_tiles_coordinates()
        self.game_over_state = False
    
    def on_size(self, widget, size):
        x, y = size
        self.SPEED = y / ORIGINAL_HEIGHT
        self.SPEED_X = x / ORIGINAL_WIDTH * 10
    
    def is_desktop(self):
        return platform in "linux win macosx".split()
    
    def get_line_x_from_index(self, index):
        central_line_x = self.perspective_point_x
        spacing = self.V_LINES_SPACING * self.width
        offset = index - 0.5
        line_x = central_line_x + offset * spacing + self.current_offset_x
        return line_x
    
    def get_line_y_from_index(self, index):
        spacing_y = self.H_LINES_SPACING * self.height
        line_y = index * spacing_y - self.current_offset_y
        return line_y
    
    def get_tile_coordinates(self, ti_x, ti_y):
        ti_y -= self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y
    
    def init_ship(self):
        with self.canvas:
            Color(0, 0, 0)
            self.ship = Triangle()
    
    def update_ship(self):
        center_x = self.width // 2
        base_y = self.SHIP_BASE_Y * self.height
        ship_half_width = self.SHIP_WIDTH * self.width // 2
        ship_height = self.SHIP_HEIGHT * self.height
    
        self.ship_coordinates[0] = center_x - ship_half_width, base_y
        self.ship_coordinates[1] = center_x, base_y + ship_height
        self.ship_coordinates[2] = center_x + ship_half_width, base_y

        x1, y1 = self.transform(*self.ship_coordinates[0])
        x2, y2 = self.transform(*self.ship_coordinates[1])
        x3, y3 = self.transform(*self.ship_coordinates[2])

        self.ship.points = [x1, y1, x2, y2, x3, y3]
    
    def check_ship_collision(self):
        for i, (ti_x, ti_y) in enumerate(self.tiles_coordinates):
            if ti_y > self.current_y_loop + 1:
                return False
            if self.check_ship_collision_with_tile(ti_x, ti_y):
                return True
        return False
    
    def check_ship_collision_with_tile(self, ti_x, ti_y):
        xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
        xmax, ymax = self.get_tile_coordinates(ti_x + 1, ti_y + 1)

        for i, (x, y) in enumerate(self.ship_coordinates):
            if x >= xmin and x <= xmax and y >= ymin and y <= ymax:
                return True
        return False
            
    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(self.V_NB_LINES):
                self.vertical_lines.append(Line())    
    
    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(self.H_NB_LINES):
                self.horizontal_lines.append(Line())
    
    def prefill_tiles_coordinates(self):
        for i in range(10):
            self.tiles_coordinates.append((0, i))

    def init_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(self.NB_TILES):
                self.tiles.append(Quad())
            
    def generate_tiles_coordinates(self):
        last_x = 0
        last_y = 0

        for i in range(len(self.tiles_coordinates) - 1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]
            
        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1
        

        for i in range(len(self.tiles_coordinates), self.NB_TILES):
            r = random.randint(0, 2)

            start_index = -int(self.V_NB_LINES // 2) + 1
            end_index = start_index + self.V_NB_LINES - 1

            if last_x <= start_index:
                r = 1
            elif last_x >= end_index:
                r = 2

            self.tiles_coordinates.append((last_x, last_y))
            if r == 1:  # right
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            elif r == 2:  # left
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))

            last_y += 1

    def update_vertical_lines(self):
        start_index = -int(self.V_NB_LINES // 2) + 1
        for i in range(start_index, start_index + self.V_NB_LINES):
            line_x = self.get_line_x_from_index(i)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]
    
    def update_horizontal_lines(self):
        start_index = -int(self.V_NB_LINES // 2) + 1
        end_index = start_index + self.V_NB_LINES - 1

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)

        for i in range(self.H_NB_LINES):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]
    
    def update_tiles(self):
        for i in range(self.NB_TILES):
            tile = self.tiles[i]
            ti_x, ti_y = self.tiles_coordinates[i]
            xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
            xmax, ymax = self.get_tile_coordinates(ti_x + 1, ti_y + 1)
            
            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update(self, dt):
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()

        if not self.game_over_state and self.game_has_started:
            self.current_offset_y += self.SPEED * time_factor
            self.current_offset_x += self.current_speed_x * time_factor

            spacing_y = self.H_LINES_SPACING * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.score_text = f"SCORE: {self.current_y_loop}"
                self.generate_tiles_coordinates()
        
            if not self.check_ship_collision():
                self.sound_music1.stop()
                self.sound_gameover_impact.play()
                Clock.schedule_once(self.play_game_over_voice_sound, 3)
                self.game_over_state = True
                self.menu_label_title = "  ".join(list("GAME OVER"))
                self.menu_button_text = "RESTART"
                self.menu_widget.opacity = 1
        
    def play_game_over_voice_sound(self, dt):
        if self.game_over_state:
            self.sound_gameover_voice.play()

    def on_menu_button_pressed(self):
        if self.game_over_state:
            self.sound_restart.play()
        else:
            self.sound_begin.play()
        self.sound_music1.play()
        self.game_has_started = True
        self.reset_state()
        self.menu_widget.opacity = 0


class GalaxyApp(App):
    pass


GalaxyApp().run()




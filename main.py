from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import *
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.graphics.transformation import Matrix
from kivy.core.window import Window

from math import sqrt, sin, cos, tan, tanh

from functools import partial

__version__ == "0.1"

class Spaceship(Scatter):
    naive_velocity = ListProperty([0.0, 0.0])
    velocity = ListProperty([0.0, 0.0])
    acceleration = ListProperty([0.0, 0.0])
    speed = NumericProperty(0.)
    naive_speed = NumericProperty(0.)

    angular_velocity = NumericProperty(0.0)
    angular_acceleration = NumericProperty(0.0)
    angle = NumericProperty(0.0)
    accel_up = BooleanProperty(False)
    accel_down = BooleanProperty(False)
    accel_left = BooleanProperty(False)
    accel_right = BooleanProperty(False)

    direction = NumericProperty()
    lorentz_followers = ListProperty([])

    def __init__(self, *args, **kwargs):
        super(Spaceship, self).__init__(*args, **kwargs)
        App.get_running_app().keyboard_widget = self
        Window.bind(on_key_up=self.on_key_up)

    def on_speed(self, *args):
        print 'self.speed is', self.speed
        print 'self.direction is', self.direction

    def update(self, dt):
        self.accelerate()
        self.move()
        if self.x < 0:
            self.naive_velocity[0] = -1*self.naive_velocity[0]
        if self.x + self.width > Window.width:
            self.naive_velocity[0] = -1*self.naive_velocity[0]
        if self.y < 0:
            self.naive_velocity[1] = -1*self.naive_velocity[1]
        if self.y + self.width > Window.height:
            self.naive_velocity[1] = -1*self.naive_velocity[1]

    def accelerate(self):
        self.naive_velocity = Vector(self.naive_velocity) + Vector(self.acceleration) 

    def move(self):
        velocity = self.velocity
        self.apply_transform(Matrix().translate(velocity[0], velocity[1], 0.0))

    def reverse(self):
        self.naive_velocity = -1*Vecotr(self.naive_velocity)

    def stop(self):
        self.acceleration = [0., 0.]
        self.naive_velocity = [0., 0.]
        self.angular_acceleration = 0.
        self.angular_velocity = 0.

    def on_key_down(self, keycode1, scancode, codepoint):
        print 'key down with keycode', keycode1
        angle = self.angle
        current_direction = Vector([sin(-angle), cos(angle)])
        if keycode1 == 273:  # up
            self.accel_up = True
        elif keycode1 == 274:  # down
            self.accel_down = True
        elif keycode1 == 275:  # right
            self.accel_right = True
        elif keycode1 == 276:  # left
            self.accel_left = True

        self.acceleration = (Vector([0., 0.1])*self.accel_up +
                             Vector([0., -0.1])*self.accel_down +
                             Vector([0.1, 0.])*self.accel_right +
                             Vector([-0.1, 0.])*self.accel_left)
            
        if keycode1 == 32:
            self.stop()

    def on_key_up(self, window, keycode1, *args):
        print 'key up with keycode', keycode1
        if keycode1 == 273:  # up
            self.accel_up = False
        elif keycode1 == 274:  # down
            self.accel_down = False
        elif keycode1 == 275:  # right
            self.accel_right = False
        elif keycode1 == 276:  # left
            self.accel_left = False

        self.acceleration = (Vector([0., 0.2])*self.accel_up +
                             Vector([0., -0.2])*self.accel_down +
                             Vector([0.2, 0.])*self.accel_right +
                             Vector([-0.2, 0.])*self.accel_left)

class GameLevel(FloatLayout):
    spaceship = ObjectProperty()
    def update(self, dt):
        if self.spaceship:
            self.spaceship.update(dt)

class LorentzBackground(FloatLayout):
    pass

class RelativityApp(App):
    game = ObjectProperty()
    keyboard_widget = ObjectProperty(None, allownone=True)
    def build(self):
        interface = GameLevel()
        Clock.schedule_interval(interface.update, 1/30.)
        Window.bind(on_key_down=self.on_key_down)
        return interface
    

    def on_key_down(self, window, keycode1, scancode, codepoint, *args):
        if keycode1 == 27 or keycode1 == 1001:
            self.manager.handle_android_back()
            return True
        elif self.keyboard_widget is not None:
            return self.keyboard_widget.on_key_down(keycode1,
                                                    scancode,
                                                    codepoint)
        return False





if __name__ == "__main__":
    RelativityApp().run()

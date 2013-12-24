from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.graphics.transformation import Matrix
from kivy.core.window import Window

from math import sqrt, sin, cos, tan

from functools import partial

class Transformer(Scatter):
    real_pos = ListProperty([0.0, 0.0])
    time_rate = NumericProperty(1.0)

    speed = ListProperty([0.0, 0.0])
    acceleration = ListProperty([0.0, 0.0])

    angular_velocity = NumericProperty(0.0)
    angular_acceleration = NumericProperty(0.0)
    angle = NumericProperty(0.0)

    length_contraction = NumericProperty(1.0)

    gamma = NumericProperty(1.0)

    def update(self, dt):
        gamma = self.gamma
        real_dt = dt * gamma

        self.accelerate()
        self.move()
        # if self.x > Window.width:
        #     self.x -= Window.width
        # if self.y > Window.height:
        #     self.y -= Window.height

    def accelerate(self):
        gamma = self.gamma
        self.velocity = Vector(self.velocity) + Vector(self.acceleration) / gamma
        self.angular_velocity += self.angular_acceleration / gamma

    def print_params(self, *args):
        print '====='
        angle = self.angle
        current_direction = Vector([sin(-angle), cos(angle)])
        print 'pos is', self.pos
        print 'current_direction', current_direction
        print 'angular velocity is', self.angular_velocity
        print 'velocity is', self.velocity
        print 'angle is', self.angle

    def move(self):
        velocity = self.velocity
        print '%%%%%%'
        print 'pos is', self.pos
        print 'velocity is', self.velocity
        self.apply_transform(Matrix().translate(velocity[0], velocity[1], 0.0))
        print 'new pos is', self.pos
        print '%%%%%%'


        ang_vel = self.angular_velocity

        self.angle += ang_vel
        self.apply_transform(Matrix().rotate(ang_vel, 0. , 0., 1.),
                             anchor=Vector(self.center))

    def reverse(self):
        self.angular_velocity = -1*self.angular_velocity

    def stop(self):
        self.acceleration = [0., 0.]
        self.velocity = [0., 0.]
        self.angular_acceleration = 0.
        self.angular_velocity = 0.


class LorentzTransformer(Transformer):
    pass


class Space(Widget):
    spaceship = ObjectProperty()
    def update(self, dt):
        if self.spaceship:
            self.spaceship.update(dt)
        
class Spaceship(Transformer):
    def __init__(self, *args, **kwargs):
        super(Spaceship, self).__init__(*args, **kwargs)
        App.get_running_app().keyboard_widget = self
    def key_handler(self, window, keycode1, keycode2,
                    text, modifiers):
        angle = self.angle
        current_direction = Vector([sin(-angle), cos(angle)])
        print keycode1
        if keycode1 == 273:  # up
            self.acceleration = Vector(self.acceleration) + 0.1 * current_direction
        elif keycode1 == 274:  # down
            self.acceleration = Vector(self.acceleration) - 0.1 * current_direction
        elif keycode1 == 275:  # right
            self.angular_velocity -= 0.01
        elif keycode1 == 276:  # left
            self.angular_velocity += 0.01
        elif keycode1 == 32:
            self.stop()

        Clock.schedule_once(self.print_params, 0.1)

class Interface(BoxLayout):
    space = ObjectProperty()
    def update(self, dt):
        if self.space:
            self.space.update(dt)

class RelativityApp(App):
    game = ObjectProperty()
    keyboard_widget = ObjectProperty(None, allownone=True)
    def build(self):
        interface = Interface()
        Clock.schedule_interval(interface.update, 1/30.)
        Window.bind(on_keyboard=self.key_handler)
        return interface
    

    def key_handler(self,window,keycode1,keycode2,text,modifiers):
        if keycode1 == 27 or keycode1 == 1001:
            self.manager.handle_android_back()
            return True
        elif self.keyboard_widget is not None:
            return self.keyboard_widget.key_handler(window,
                                                    keycode1,
                                                    keycode2,
                                                    text,
                                                    modifiers)
        return False





if __name__ == "__main__":
    RelativityApp().run()

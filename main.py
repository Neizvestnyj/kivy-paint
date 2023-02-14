from kivy.config import Config

Config.set('kivy', 'window_icon', 'logo.ico')  # NOQA
Config.set('input', 'mouse', 'mouse,disable_multitouch')  # NOQA
Config.set('kivy', 'exit_on_escape', 0)  # NOQA

from kivymd.app import MDApp
from kivymd.uix.widget import MDWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.behaviors.touch_behavior import TouchBehavior
from kivymd.uix.pickers import MDColorPicker

from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.properties import StringProperty, OptionProperty, NumericProperty
from kivy.input.providers.mouse import MouseMotionEvent
from kivy.lang.builder import Builder
from kivy.core.window import Window

from typing import Union


class Toolbar(MDBoxLayout):
    pass


class ToolButton(TouchBehavior, MDIconButton):
    method = StringProperty()


class PaintWidget(MDWidget):
    type = OptionProperty('line', options=['line', 'circle', 'point', 'square', 'fill'])
    """
    Drawing method
    """

    line_width = NumericProperty(3)
    """
    Line length
    """

    circle_radius = NumericProperty(10)
    """
    Circle radius
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget_color = self.theme_cls.primary_color

    def check_collision(self, pos: list) -> bool:
        """
        :param pos: `touch.pos`
        :return: `bool`
        In fact, it does not allow you to draw on the ToolBar
        """

        if self.type == 'line' and self.collide_point(pos[0] + self.line_width, pos[1] + self.line_width):
            return True

        if self.type == 'circle' and self.collide_point(pos[0], pos[1] + self.circle_radius + self.line_width):
            return True

        if self.type == 'square' and self.collide_point(pos[0], pos[1] + self.circle_radius + self.line_width):
            return True

        if self.type == 'point' and self.collide_point(pos[0], pos[1] + self.circle_radius / 2):
            return True

        if self.type == 'fill' and self.collide_point(*pos):
            return True

        return False

    def on_touch_down(self, touch: MouseMotionEvent):
        # Don't draw on other widget
        if not touch.is_mouse_scrolling and touch.pos and self.check_collision(touch.pos):
            if self.type == 'line':
                with self.canvas.after:
                    Color(*self.widget_color, mode='rgba')
                    touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.line_width)

            elif self.type == 'circle':
                with self.canvas.after:
                    Color(*self.widget_color, mode='rgba')
                    # (center_x, center_y, radius, angle_start, angle_end, segments)
                    touch.ud['line'] = Line(circle=(touch.x, touch.y, self.circle_radius),
                                            width=self.line_width,
                                            )

            elif self.type == 'point':
                with self.canvas.after:
                    Color(*self.widget_color, mode='rgba')
                    d = self.circle_radius
                    Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))

            elif self.type == 'square':
                with self.canvas.after:
                    Color(*self.widget_color, mode='rgba')
                    # (x, y, width, height)
                    touch.ud['line'] = Line(rectangle=(touch.x, touch.y, self.circle_radius, self.circle_radius),
                                            width=self.line_width,
                                            )

            elif self.type == 'fill':
                with self.canvas.after:
                    Color(*self.widget_color, mode='rgba')
                    # (x, y, width, height)
                    Rectangle(size=self.size, pos=self.pos)

            else:
                raise TypeError

    def on_touch_move(self, touch: MouseMotionEvent):
        if 'line' in touch.ud and touch.pos and self.check_collision(touch.pos):
            touch.ud['line'].points += (touch.x, touch.y)

    def clear(self):
        """
        :return:
        Clear canvas
        """

        self.canvas.after.clear()


class PaintApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = 'logo.png'
        Window.maximize()

        self.color_picker = None
        self.screen = Builder.load_file('Paint.kv')

    def build(self):
        return self.screen

    def set_draw_method(self, method: str):
        self.root.ids.painter.type = method

    def set_line_width(self, width: str):
        if width:
            self.root.ids.painter.line_width = int(width)

    def set_circle_radius(self, radius: str):
        if radius:
            self.root.ids.painter.circle_radius = int(radius)

    def clear_canvas(self):
        self.root.ids.painter.clear()

    def open_color_picker(self):
        if not self.color_picker:
            self.color_picker = MDColorPicker(size_hint=(0.45, 0.85))
            self.color_picker.bind(
                on_select_color=self.on_select_color,
                on_release=self.get_selected_color,
            )

        self.color_picker.open()

    def update_color(self, color: list) -> None:
        """
        :param color: rgba color
        :return:
        """

        self.root.ids.painter.widget_color = color
        print(self.root.ids.painter.widget_color, color)

    def get_selected_color(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        """
        :param instance_color_picker: `MDColorPicker`
        :param type_color: `RGBA`, `HEX`, `RGB`.
        :param selected_color:
        :return:
        Return selected color
        """

        self.update_color(selected_color[:-1] + [1])

    def on_select_color(self, instance_gradient_tab: MDColorPicker, color: list) -> None:
        """
        :param instance_gradient_tab: `MDColorPicker`
        :param color: rgba
        :return:
        Called when a gradient image is clicked
        """


if __name__ == '__main__':
    PaintApp().run()

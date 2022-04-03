"""Experimenting with scaling sprites for a moving magnifier."""

import copy
import pyglet
from pyglet.gl import *
from rich.traceback import install
from loguru import logger

install(show_locals=True)


glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
# glScalef(1.0, 1.0, 1.0)
# image = pyglet.image.load('media/cat/xray/cat_views.png')

# scale_factor = image.height / 720
# image.height = 720
# image.width = image.width / scale_factor


image = pyglet.resource.image('media/cat/xray/cat_views.png')
orig_image = copy.copy(image)
#orig_image = pyglet.resource.image('media/cat/xray/cat_views.png')
logger.debug(f"image start w:{image.width} h:{image.height}")
logger.debug(f"orig_image start w:{orig_image.width} h:{orig_image.height}")

height, width = 720, 1280  # Desired resolution

scale_y = min(image.height, height) / max(image.height, height)
scale_x = min(width, image.width) / max(width, image.width)
# image.scale_x = scale_x
# image.scale_y = scale_y
image.scale = min(scale_x, scale_y)

# Usually not needed, and should not be tampered with,
# but for a various bugs when using sprite-inheritance on a user-defined
# class, these values will need to be updated manually:
image.width = width  # * scale_x
image.height = height  # * scale_y
# image.texture.width = width
# image.texture.height = height
logger.debug(f"image now w:{image.width} h:{image.height}")
logger.debug(f"orig_image now w:{orig_image.width} h:{orig_image.height}")

# ball_image = pyglet.image.load('ball.png')
cat = pyglet.sprite.Sprite(image, x=100, y=100)

display = pyglet.canvas.get_display()
screens = display.get_screens()
for i, screen in enumerate(screens):
    print(f"Screen #{i}: {screen}")
screen = screens[0]


class MagWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mag_pos = [0, 0]

    def on_draw(self):
        window.clear()
        image.blit(0, 0, 0)
        # y=24 fine, y=25 seg fault
        mag_image = orig_image.get_region(
            x=self.mag_pos[0] // image.scale,
            y=self.mag_pos[1] // image.scale,
            width=100,
            height=100)
        # print(window.width, window.height)
        # removing this removes segfault
        # cat.draw()
        label.draw()
        mag_image.blit(self.mag_pos[0], self.mag_pos[1], 0)

    def on_mouse_press(self, x, y, button, modifiers):
        self.mag_pos[0] = x
        self.mag_pos[1] = y
        logger.debug(f"Mouse press x:{x} y:{y}")

    def on_key_press(self, symbol, modifiers):
        """Pressing any key exits app."""
        if symbol == pyglet.window.key.P:
            print("p pressed")
        else:
            pyglet.app.exit()


style = pyglet.window.Window.WINDOW_STYLE_DEFAULT
window = MagWindow(1280, 720, caption="Mag Test Window",
                   screen=screen, style=style, fullscreen=False)
# cursor = window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
# window.set_mouse_cursor(cursor)
# window.set_visible(True)

label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width // 2, y=window.height // 2,
                          anchor_x='center', anchor_y='center')


def update(dt):
    # Move 10 pixels per second
    #cat.x += dt * 10
    window.mag_pos[0] += 1
    window.mag_pos[1] += 1


# Call update 60 times a second
pyglet.clock.schedule_interval(update, 1 / 60.)

pyglet.app.run()

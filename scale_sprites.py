"""Experimenting with scaling sprites for a moving magnifier."""

import pyglet
from pyglet.gl import *

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

image = pyglet.image.load('media/cat/xray/cat_views.png')
# image = pyglet.resource.image('media/cat/xray/001.jpg')
height, width = 800, 600  # Desired resolution

# the min() and max() mumbo jumbo is to honor the smallest requested resolution.
# this is because the smallest resolution given is the limit of say
# the window-size that the image will fit in, there for we can't honor
# the largest resolution or else the image will pop outside of the region.
# image.scale = min(image.height, height) / max(image.height,
#                                               height), min(width, image.width) / max(width, image.width)

# Usually not needed, and should not be tampered with,
# but for a various bugs when using sprite-inheritance on a user-defined
# class, these values will need to be updated manually:
# image.width = width
# image.height = height
# image.texture.width = width
# image.texture.height = height


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

    def on_draw(self):
        window.clear()
        image.blit(0, 0, 0)
        # y=24 fine, y=25 seg fault
        mag_image = image.get_region(
            x=mag_pos[0], y=mag_pos[1], width=100, height=100)
        # print(window.width, window.height)
        # removing this removes segfault
        mag_image.blit(mag_pos[0], mag_pos[1], 0)
        # cat.draw()
        label.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        mag_pos[0] = x
        mag_pos[1] = y
        print("mouse press")


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

mag_pos = [0, 0]


def update(dt):
    # Move 10 pixels per second
    label.x += dt * 10
    #mag_pos[0] += 20
    #mag_pos[1] += 20


# Call update 60 times a second
pyglet.clock.schedule_interval(update, 1 / 60.)

pyglet.app.run()

"""Experimenting with scaling sprites for a moving magnifier."""

import copy
import pyglet
from pyglet.gl import *
from rich.traceback import install
from loguru import logger

install(show_locals=True)


glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
# glScalef(1.0, 1.0, 1.0)

image = pyglet.resource.image('media/cat/xray/cat_views.png')
orig_image = copy.copy(image)
logger.debug(f"image start w:{image.width} h:{image.height}")
logger.debug(f"orig_image start w:{orig_image.width} h:{orig_image.height}")

height, width = 720, 1280  # Desired resolution

scale_y = min(image.height, height) / max(image.height, height)
scale_x = min(width, image.width) / max(width, image.width)
image.scale = min(scale_x, scale_y)
logger.debug(f"Scales x:{scale_x} y:{scale_y} min:{image.scale}")

image.width = image.width * image.scale
image.height = image.height * image.scale
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

RET_SIDE = 200  # Length of side of reticle box
RET_BOX_WT = 10  # Line weight of reticle box lines


class MagWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mag_pos = [0, 0]
        self.mag_x = 0
        self.mag_y = 0
        self.reticle_batch = pyglet.graphics.Batch()
        self.ret_left = pyglet.shapes.Line(self.mag_x, self.mag_y, self.mag_x, self.mag_y + RET_SIDE, width=10,
                                           color=(200, 20, 20), batch=self.reticle_batch)
        self.ret_right = pyglet.shapes.Line(self.mag_x + RET_SIDE, self.mag_y, self.mag_x + RET_SIDE, self.mag_y + RET_SIDE, width=10,
                                            color=(200, 20, 20), batch=self.reticle_batch)
        self.ret_top = pyglet.shapes.Line(self.mag_x - RET_BOX_WT // 2, self.mag_y + RET_SIDE, self.mag_x + RET_SIDE + RET_BOX_WT // 2, self.mag_y + RET_SIDE, width=10,
                                          color=(200, 20, 20), batch=self.reticle_batch)
        self.ret_bot = pyglet.shapes.Line(self.mag_x - RET_BOX_WT // 2, self.mag_y, self.mag_x + RET_SIDE + RET_BOX_WT // 2, self.mag_y, width=10,
                                          color=(200, 20, 20), batch=self.reticle_batch)

    def on_draw(self):
        window.clear()
        image.blit(0, 0, 0)
        mag_image = orig_image.get_region(
            # Subtract half of RET_SIDE to center magnified image on cursor
            x=self.mag_x // image.scale,  # - RET_SIDE // 2,
            y=self.mag_y // image.scale,  # - RET_SIDE // 2,
            width=RET_SIDE,
            height=RET_SIDE)
        mag_image.blit(self.mag_x, self.mag_y, 0)
        self.reticle_batch.draw()

    def on_mouse_motion(self, x, y, button, modifiers):
        self.mag_x = x
        self.mag_y = y
        # logger.debug(f"Mouse press x:{x} y:{y}")

    def on_key_press(self, symbol, modifiers):
        """Pressing any key exits app."""
        if symbol == pyglet.window.key.D:
            print("d pressed")
            self.mag_x += 10
        elif symbol == pyglet.window.key.A:
            print("a pressed")
            self.mag_x -= 10
        elif symbol == pyglet.window.key.W:
            print("w pressed")
            self.mag_y += 10
        elif symbol == pyglet.window.key.S:
            print("s pressed")
            self.mag_y -= 10
        else:
            logger.info(f"Other key press, exiting: {symbol}")
            pyglet.app.exit()

    def update(self, dt):
        """Move position of magnifying image, and lines making rect."""
        # Move position used to get magnified region of image.
        # TODO: If randomly moving, keep within bounds of memory.
        # self.mag_x += 50 * dt  # Move 50px per second
        # self.mag_y += 50 * dt

        # Move lines making up reticle rectangle
        self.ret_left.x = self.mag_x
        self.ret_left.y = self.mag_y
        self.ret_left.x2 = self.mag_x
        self.ret_left.y2 = self.mag_y + RET_SIDE
        self.ret_right.x = self.mag_x + RET_SIDE
        self.ret_right.y = self.mag_y
        self.ret_right.x2 = self.mag_x + RET_SIDE
        self.ret_right.y2 = self.mag_y + RET_SIDE
        self.ret_top.x = self.mag_x - RET_BOX_WT // 2
        self.ret_top.y = self.mag_y + RET_SIDE
        self.ret_top.x2 = self.mag_x + RET_SIDE + RET_BOX_WT // 2
        self.ret_top.y2 = self.mag_y + RET_SIDE
        self.ret_bot.x = self.mag_x - RET_BOX_WT // 2
        self.ret_bot.y = self.mag_y
        self.ret_bot.x2 = self.mag_x + RET_SIDE + RET_BOX_WT // 2
        self.ret_bot.y2 = self.mag_y


style = pyglet.window.Window.WINDOW_STYLE_DEFAULT
window = MagWindow(1280, 720, caption="Mag Test Window",
                   screen=screen, style=style, fullscreen=True)

# Call update 60 times a second
pyglet.clock.schedule_interval(window.update, 1 / 60.)

pyglet.app.run()

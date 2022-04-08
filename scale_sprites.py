"""Experimenting with scaling sprites for a moving magnifier."""

import copy

import pyglet
from loguru import logger
from pyglet.gl import *
from rich.traceback import install

install(show_locals=True)


glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
# glScalef(1.0, 1.0, 1.0)

image = pyglet.resource.image("media/cat/xray/cat_views.png")
orig_image = copy.copy(image)
logger.debug(f"image start w:{image.width} h:{image.height}")
logger.debug(f"orig_image start w:{orig_image.width} h:{orig_image.height}")

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080  # window resolution

# Main animal image display section
AN_WIDTH, AN_HEIGHT = 1280, 720  # size of animal window
AN_X, AN_Y = 0, SCREEN_HEIGHT - AN_HEIGHT  # origin of animal window

# Magnifier display section, fixed at MD_X, MD_Y
MD_WIDTH, MD_HEIGHT = 640, 320
MD_X, MD_Y = 0, 0


DIV_WT = 10

scale_y = min(image.height, AN_HEIGHT) / max(image.height, AN_HEIGHT)
scale_x = min(AN_WIDTH, image.width) / max(AN_WIDTH, image.width)
image.scale = min(scale_x, scale_y)
logger.debug(f"Scales x:{scale_x} y:{scale_y} min:{image.scale}")

image.width = image.width * image.scale
image.height = image.height * image.scale
# image.texture.width = width
# image.texture.height = height
logger.debug(f"image now w:{image.width} h:{image.height}")
logger.debug(f"orig_image now w:{orig_image.width} h:{orig_image.height}")

RET_WIDTH = MD_WIDTH * image.scale
RET_HEIGHT = MD_HEIGHT * image.scale

# RET_SIDE = 200  # Length of side of reticle box
RET_BOX_WT = 10  # Line weight of reticle box lines


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

        # self.mag_pos = [0, 0]
        self.mag_x = AN_X
        self.mag_y = AN_Y
        self.reticle_batch = pyglet.graphics.Batch()

        # Rectangle around moving reticle
        self.ret_left = pyglet.shapes.Line(
            self.mag_x,
            self.mag_y,
            self.mag_x,
            self.mag_y + RET_HEIGHT,
            width=10,
            color=(200, 20, 20),
            batch=self.reticle_batch,
        )
        self.ret_right = pyglet.shapes.Line(
            self.mag_x + RET_WIDTH,
            self.mag_y,
            self.mag_x + RET_WIDTH,
            self.mag_y + RET_HEIGHT,
            width=10,
            color=(200, 20, 20),
            batch=self.reticle_batch,
        )
        self.ret_top = pyglet.shapes.Line(
            self.mag_x - RET_BOX_WT // 2,
            self.mag_y + RET_HEIGHT - DIV_WT // 2,
            self.mag_x + RET_WIDTH + RET_BOX_WT // 2,
            self.mag_y + RET_HEIGHT - DIV_WT // 2,
            width=10,
            color=(200, 20, 20),
            batch=self.reticle_batch,
        )
        self.ret_bot = pyglet.shapes.Line(
            self.mag_x - RET_BOX_WT // 2,
            self.mag_y,
            self.mag_x + RET_WIDTH + RET_BOX_WT // 2,
            self.mag_y,
            width=10,
            color=(200, 20, 20),
            batch=self.reticle_batch,
        )

        # Divide screen with lines
        # self.division_batch = pyglet.graphics.Batch()

        # Rectangle around magnifier display
        self.mag_disp_left = pyglet.shapes.Line(
            MD_X + DIV_WT // 2,
            MD_Y,
            MD_X + DIV_WT // 2,
            MD_Y + MD_HEIGHT,
            color=(200, 20, 20),
            batch=self.reticle_batch,
            width=DIV_WT,
        )
        self.mag_disp_right = pyglet.shapes.Line(
            MD_X + MD_WIDTH - DIV_WT // 2,
            MD_Y,
            MD_X + MD_WIDTH - DIV_WT // 2,
            MD_Y + MD_HEIGHT,
            color=(200, 20, 20),
            batch=self.reticle_batch,
            width=DIV_WT,
        )
        self.mag_disp_top = pyglet.shapes.Line(
            MD_X,
            MD_Y + MD_HEIGHT - DIV_WT // 2,
            MD_X + MD_WIDTH,
            MD_Y + MD_HEIGHT - DIV_WT // 2,
            color=(200, 20, 20),
            batch=self.reticle_batch,
            width=DIV_WT,
        )
        self.mag_disp_bottom = pyglet.shapes.Line(
            MD_X,
            MD_Y,
            MD_X + MD_WIDTH,
            MD_Y,
            color=(200, 20, 20),
            batch=self.reticle_batch,
            width=DIV_WT,
        )

        # Rectangle around main animal window
        self.screen_left = pyglet.shapes.Line(
            AN_X + DIV_WT // 2,
            AN_Y,
            AN_X + DIV_WT // 2,
            AN_Y + AN_HEIGHT,
            color=(200, 20, 20),
            batch=self.reticle_batch,
            width=DIV_WT,
        )
        self.screen_right = pyglet.shapes.Line(
            AN_X + AN_WIDTH - DIV_WT // 2,
            AN_Y,
            AN_X + AN_WIDTH - DIV_WT // 2,
            AN_Y + AN_HEIGHT,
            color=(200, 20, 20),
            batch=self.reticle_batch,
            width=DIV_WT,
        )
        self.screen_top = pyglet.shapes.Line(
            AN_X,
            AN_Y + AN_HEIGHT - DIV_WT // 2,
            AN_X + AN_WIDTH,
            AN_Y + AN_HEIGHT - DIV_WT // 2,
            color=(200, 20, 20),
            batch=self.reticle_batch,
            width=DIV_WT,
        )
        self.screen_bottom = pyglet.shapes.Line(
            AN_X,
            AN_Y,
            AN_X + AN_WIDTH,
            AN_Y,
            color=(200, 20, 20),
            batch=self.reticle_batch,
            width=DIV_WT,
        )

        # Lines linking reticle to magnification display section
        LINK_LINE_COLOR = (200, 20, 20)
        LINK_LINE_WIDTH = 2
        self.tl_link = pyglet.shapes.Line(
            MD_X,
            MD_Y,
            self.mag_x,
            self.mag_y,
            color=LINK_LINE_COLOR,
            batch=self.reticle_batch,
            width=LINK_LINE_WIDTH,
        )

        self.tr_link = pyglet.shapes.Line(
            MD_X + MD_WIDTH,
            MD_Y,
            self.mag_x + MD_WIDTH,
            self.mag_y,
            color=LINK_LINE_COLOR,
            batch=self.reticle_batch,
            width=LINK_LINE_WIDTH,
        )

        self.ll_link = pyglet.shapes.Line(
            MD_X,
            MD_Y + MD_HEIGHT,
            self.mag_x,
            self.mag_y,
            color=LINK_LINE_COLOR,
            batch=self.reticle_batch,
            width=LINK_LINE_WIDTH,
        )

        self.lr_link = pyglet.shapes.Line(
            MD_X + MD_WIDTH,
            MD_Y + MD_HEIGHT,
            self.mag_x + RET_WIDTH,
            self.mag_y,
            color=LINK_LINE_COLOR,
            batch=self.reticle_batch,
            width=LINK_LINE_WIDTH,
        )

    def on_draw(self):
        window.clear()
        image.blit(AN_X, AN_Y, 0)
        mag_image = orig_image.get_region(
            # Subtract half of RET_SIDE to center magnified image on cursor
            x=(self.mag_x - AN_X) // image.scale,  # - RET_SIDE // 2,
            y=(self.mag_y - AN_Y) // image.scale,  # - RET_SIDE // 2,
            width=RET_WIDTH // image.scale,
            height=RET_HEIGHT // image.scale,
        )
        # mag_image.blit(self.mag_x, self.mag_y, 0)
        mag_image.blit(MD_X, MD_Y, 0)
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
        self.ret_left.y2 = self.mag_y + RET_HEIGHT
        self.ret_right.x = self.mag_x + RET_WIDTH
        self.ret_right.y = self.mag_y
        self.ret_right.x2 = self.mag_x + RET_WIDTH
        self.ret_right.y2 = self.mag_y + RET_HEIGHT
        self.ret_top.x = self.mag_x - RET_BOX_WT // 2
        self.ret_top.y = self.mag_y + RET_HEIGHT
        self.ret_top.x2 = self.mag_x + RET_WIDTH + RET_BOX_WT // 2
        self.ret_top.y2 = self.mag_y + RET_HEIGHT
        self.ret_bot.x = self.mag_x - RET_BOX_WT // 2
        self.ret_bot.y = self.mag_y
        self.ret_bot.x2 = self.mag_x + RET_WIDTH + RET_BOX_WT // 2
        self.ret_bot.y2 = self.mag_y

        self.tl_link.x2 = self.mag_x
        self.tl_link.y2 = self.mag_y
        self.tr_link.x2 = self.mag_x + RET_WIDTH
        self.tr_link.y2 = self.mag_y
        self.ll_link.x2 = self.mag_x
        self.ll_link.y2 = self.mag_y + RET_HEIGHT
        self.lr_link.x2 = self.mag_x + RET_WIDTH
        self.lr_link.y2 = self.mag_y + RET_HEIGHT


style = pyglet.window.Window.WINDOW_STYLE_DEFAULT
window = MagWindow(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    caption="Mag Test Window",
    screen=screen,
    style=style,
    fullscreen=True,
)

# Call update 60 times a second
pyglet.clock.schedule_interval(window.update, 1 / 60.0)

pyglet.app.run()

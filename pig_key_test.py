#!/usr/bin/env python3
from __future__ import print_function
import time
from datetime import datetime
import mercury
import log
import pyglet
import os
from pyglet.event import EventDispatcher


# #reader = mercury.Reader("llrp://izar-51e4c8.local", protocol="GEN2")
# reader = mercury.Reader("tmr:///com2", protocol="GEN2")

# print(reader.get_model())
# print(reader.get_supported_regions())

# # Adding bank= causes segmentation fault, maybe tags don't support
# reader.set_read_plan([1, 2], "GEN2", read_power=1900)
# # print(reader.read())


os.environ['DISPLAY'] = ':1'
window = pyglet.window.Window()
image = pyglet.resource.image('media/dog/xray/001.png')

label = pyglet.text.Label('Neigh/Woof/Meow',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')


class TagDispatcher(EventDispatcher):
    def tag_read(self, epc):
        self.dispatch_event('on_tag_read', epc.epc)

    def on_tag_read(self, epc):
        print("TagDispatcher Dispatched: ", epc.epc)


TagDispatcher.register_event_type('on_tag_read')
td = TagDispatcher()


@window.event
def on_draw():
    pass
    # window.clear()
    # image.blit(0, 0)
    # label.draw()


@window.event
def on_tag_read(epc):
    print("Window rx epc: ", epc)
    label = pyglet.text.Label(epc.epc,
                              font_name='Times New Roman',
                              font_size=36,
                              x=window.width//2, y=window.height//2,
                              anchor_x='center', anchor_y='center')
    label.draw()
    pyglet.clock.schedule_once(callback, 1)        # called in 5 seconds


@window.event
def callback(dt):
    print(dt, " seconds since.")
    window.clear()
    image.blit(0, 0)


@window.event
def on_key_press(symbol, modifiers):
    window.clear()


@window.event
def on_key_release(symbol, modifiers):
    label = pyglet.text.Label("Keypress!",
                              font_name='Times New Roman',
                              font_size=36,
                              x=window.width//2, y=window.height//2,
                              anchor_x='center', anchor_y='center')
    label.draw()
    pyglet.clock.schedule_once(callback, 5)        # called in 5 seconds


# reader.start_reading(log.log_tag)
# reader.start_reading(td.tag_read)

pyglet.app.run()

# reader.stop_reading()

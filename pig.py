#!/usr/bin/env python3
from __future__ import print_function
import time
from datetime import datetime
import mercury
import log
import pyglet
import os
from pyglet.event import EventDispatcher
import epc


reader = mercury.Reader("llrp://izar-51e4c8.local", protocol="GEN2")


print(reader.get_model())
print(reader.get_supported_regions())

# Adding bank= causes segmentation fault, maybe tags don't support
reader.set_read_plan([1, 2], "GEN2", read_power=1900)
# print(reader.read())


class TagDispatcher(EventDispatcher):
    def tag_read(self, bepc):
        self.dispatch_event('on_tag_read', epc.epc_to_string(bepc))

    def on_tag_read(self, bepc):
        print("TagDispatcher Dispatched: ", epc.epc_to_string(bepc))


TagDispatcher.register_event_type('on_tag_read')
td = TagDispatcher()


#os.environ['DISPLAY'] = ':1'
window = pyglet.window.Window()
image = pyglet.resource.image('media/dog/xray/001.png')

label = pyglet.text.Label('Neigh/Woof/Meow',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')


@window.event
def on_draw():
    # window.clear()
    # image.blit(0, 0)
    # label.draw()
    pass


@window.event
def on_tag_read(epc):
    print("Window rx epc: ", epc)
    label = pyglet.text.Label(epc,
                              font_name='Times New Roman',
                              font_size=36,
                              x=window.width//2, y=window.height//2,
                              anchor_x='center', anchor_y='center')
    label.draw()


@window.event
def on_key_release(symbol, modifiers):
    label = pyglet.text.Label(str(symbol),
                              font_name='Times New Roman',
                              font_size=36,
                              x=window.width//2, y=window.height//2,
                              anchor_x='center', anchor_y='center')
    # label.draw()


# reader.start_reading(log.log_tag)
reader.start_reading(td.tag_read)

pyglet.app.run()

reader.stop_reading()

#!/usr/bin/env python3
from __future__ import print_function
import time
from datetime import datetime
import mercury
import log
import pyglet
import os
from pyglet.event import EVENT_HANDLED, EventDispatcher
import epc


reader = mercury.Reader("llrp://izar-51e4c8.local", protocol="GEN2")
# reader = mercury.Reader("tmr:///com2", protocol="GEN2")

print(reader.get_model())
print(reader.get_supported_regions())

# Adding bank= causes segmentation fault, maybe tags don't support
reader.set_read_plan([1, 2], "GEN2", read_power=1900)
# print(reader.read())

dog = pyglet.resource.image('media/dog/xray/001.png')
cat = pyglet.resource.image('media/cat/xray/001.jpg')
horse = pyglet.resource.image('media/horse/xray/001.jpg')

text_for_label = "external variable"

ext_label = pyglet.text.Label("External label",
                              color=(255, 0, 0, 255),
                              font_size=12)


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_batch = pyglet.graphics.Batch()
        self.label = pyglet.text.Label("Test!",
                                       batch=self.label_batch,
                                       color=(255, 0, 0, 255),
                                       font_size=12,
                                       x=self.width//2, y=self.height//3,
                                       anchor_x='center', anchor_y='center')
        self.image = dog

    def on_tag_read(self, epc):
        self.clear()
        self.image = cat
        print("Window Class rx epc: ", epc)
        new_text = "Rx from new_text"

        self.flip()  # Required to cause window refresh
        # called in 5 seconds
        pyglet.clock.schedule_once(self.callback, 5)
        pyglet.clock.schedule_once(self.label_change, 0, "Silly")
        # self.label_change(0, "not really") # Does not work

        # return EVENT_HANDLED

    def label_change(self, dt, label_text):
        self.label = pyglet.text.Label(text=label_text,
                                       color=(255, 0, 0, 255),
                                       font_size=12,
                                       x=self.width//2, y=self.height//3,
                                       anchor_x='center', anchor_y='center')
        self.label.draw()

    def on_key_release(self, symbol, modifiers):
        print("Window RX Keypress")
        self.clear()
        self.image = horse
        # self.label.text("Keypress!")
        self.label = pyglet.text.Label("Keys, keys, keys!",
                                       color=(255, 0, 0, 255),
                                       font_size=12)
        self.label.draw()
        # called in 5 seconds
        pyglet.clock.schedule_once(self.callback, 5)

    def callback(self, dt):
        print(dt, " seconds since.")
        # self.clear()
        self.image = dog
        self.label = pyglet.text.Label("idle, idle, idle!",
                                       color=(255, 0, 0, 255),
                                       font_size=12,
                                       x=self.width//2, y=self.height//3,
                                       anchor_x='center', anchor_y='center')
        self.label.draw()

    def on_key_press(self, symbol, modifiers):
        self.clear()

    def on_draw(self):
        self.clear()
        self.image.blit(0, 0)
        self.label.draw()
        # self.label_batch.draw()
        print("on draw label text: ", self.label.text)
        # self.flip()


class TagDispatcher(EventDispatcher):
    def __init__(self, window1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window1 = window1

    def read_tags(self, dt):
        print("td read tags: ", reader.read())
        epc_string = "TEST_EPC_STRING"
        # epc_strings = [epc.epc_to_string(bepc) for bepc in list(reader.read())]
        # if epc_strings:
        #     print("epc_strings")
        #     for epc in epc_strings:
        #         pass
        self.window1.dispatch_event('on_tag_read', epc_string)

    def tag_read(self, bepc):
        epc_string = epc.epc_to_string(bepc)
        # print("Tag read: ", epc_string)
        # self.dispatch_event('on_tag_read', epc_string)
        self.window1.dispatch_event('on_tag_read', epc_string)

    def on_tag_read(self, epc):
        # print("TagDispatcher Dispatched: ", epc)
        pass


MyWindow.register_event_type('on_tag_read')
TagDispatcher.register_event_type('on_tag_read')


# os.environ['DISPLAY'] = ':1'
window = MyWindow(600, 600, "Pet U", True)
event_logger = pyglet.window.event.WindowEventLogger()
window.push_handlers(event_logger)


td = TagDispatcher(window)


# reader.start_reading(log.log_tag)
# reader.start_reading(td.tag_read)
pyglet.clock.schedule_interval(td.read_tags, 1)   # called once a second
pyglet.app.run()

# reader.stop_reading()

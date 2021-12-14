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
import files
import species


reader = mercury.Reader("llrp://izar-51e4c8.local", protocol="GEN2")
# reader = mercury.Reader("tmr:///com2", protocol="GEN2")

print(reader.get_model())
print(reader.get_supported_regions())

# Adding bank= causes segmentation fault, maybe tags don't support
reader.set_read_plan([1, 2], "GEN2", read_power=1000)
# print(reader.read())

dog = pyglet.resource.image('media/dog/xray/001.png')
cat = pyglet.resource.image('media/cat/xray/001.jpg')
horse = pyglet.resource.image('media/horse/xray/001.jpg')

clock = pyglet.clock.get_default()


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.label_batch = pyglet.graphics.Batch()
        self.label = pyglet.text.Label("Test!",
                                       # batch=self.label_batch,
                                       color=(255, 0, 0, 255),
                                       font_size=12,
                                       x=self.width//2, y=self.height//3,
                                       anchor_x='center', anchor_y='center')
        self.image = dog

    def on_tag_read(self, tag):
        self.clear()
        self.image = cat
        spec = species.species_str(epc.epc_species_num(tag)).lower()
        media_dir = 'xray'
        media_type = 'img'
        self.image = files.random_species_dir_type(spec, media_dir, media_type)
        print("Window Class rx epc: ", tag)
        # clock.schedule_once(self.label_change, 0, tag) workaround before label change worked
        self.label = pyglet.text.Label(text=tag,
                                       color=(255, 0, 0, 255),
                                       font_size=36,
                                       x=self.width//2, y=self.height//2,
                                       anchor_x='center', anchor_y='center')
        self.label.draw()

        self.flip()  # Required to cause window refresh
        log.log_tag(tag)
        return EVENT_HANDLED

    # def label_change(self, dt, label_text):
    #     print("Seconds before label change: ", dt)
    #     self.label = pyglet.text.Label(text=label_text,
    #                                    color=(255, 0, 0, 255),
    #                                    font_size=36,
    #                                    x=self.width//2, y=self.height//2,
    #                                    anchor_x='center', anchor_y='center')
    #     self.label.draw()

    def on_key_press(self, symbol, modifiers):
        self.clear()
        self.flip()

    def on_key_release(self, symbol, modifiers):
        print("Window RX Keypress")
        self.clear()
        self.image = horse
        self.label = pyglet.text.Label("Keys, keys, keys!",
                                       color=(255, 0, 0, 255),
                                       x=self.width//2, y=self.height//2,
                                       font_size=12)
        self.label.draw()
        clock.schedule_once(self.idle, 2)

    def idle(self, dt):
        clock.unschedule(self.idle)
        print("Going idle, ", dt, " seconds since scan.")
        self.clear()  # why was this commented out?
        self.image = None
        self.label = pyglet.text.Label('Please place the patient in the scanning area.',
                                       color=(255, 255, 255, 255),
                                       font_size=24,
                                       x=self.width//2, y=self.height//2,
                                       anchor_x='center', anchor_y='center')
        self.label.draw()

    def on_draw(self):
        self.clear()
        if self.image:
            self.image.blit(0, 0)
        self.label.draw()
        # self.label_batch.draw()
        #print("on draw label text: ", self.label.text)
        # self.flip()


class TagDispatcher(EventDispatcher):
    def __init__(self, window1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window1 = window1

    def read_tags(self, dt):
        tag_list = reader.read()
        if tag_list:
            clock.unschedule(self.window1.idle)
            for tag in tag_list:
                print("Read EPC: ", epc.epc_to_string(
                    tag), ", RSSI: ", tag.rssi)
            tag_list.sort(key=lambda tag: tag.rssi)
            best_tag = tag_list[0]
            best_tag_string = epc.epc_to_string(best_tag)
            print("Highest signal from read: ", best_tag_string)
            self.window1.dispatch_event('on_tag_read', best_tag_string)
            print("Dispacted tag: ", best_tag_string)
            # TODO send tag to correct monitors
        else:
            # TODO Idle monitors of empty antennas.
            
            clock.schedule_once(self.window1.idle, 1)

    def tag_read(self, tag):
        epc_string = epc.epc_to_string(tag)
        # print("Tag read: ", epc_string)
        self.window1.dispatch_event('on_tag_read', epc_string)

    def on_tag_read(self, epc):
        # I don't think we need this function
        # print("TagDispatcher Dispatched: ", epc)
        pass


MyWindow.register_event_type('on_tag_read')
TagDispatcher.register_event_type('on_tag_read')


window = MyWindow(900, 800, "Pet U", True)
# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)


td = TagDispatcher(window)


# reader.start_reading(log.log_tag)
# reader.start_reading(td.tag_read)
clock.schedule_interval(td.read_tags, 0.1)   # called once a second
pyglet.app.run()

# reader.stop_reading()

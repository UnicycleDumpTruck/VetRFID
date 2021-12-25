#!/usr/bin/env python3
"""Subclassing pyglet Window to add behavior."""
from __future__ import annotations
from datetime import datetime
import pyglet  # type: ignore
import files
import epc
import log


class ScannerWindow(pyglet.window.Window):
    """Subclassing pyglet Window to add logic and display."""

    def __init__(self, *args, window_number, antennas, **kwargs):
        """Set up backgroud and periphery labels."""
        super().__init__(*args, **kwargs)
        self.background_graphics = []
        self.graphics = []
        self.graphics_batch = pyglet.graphics.Batch()
        self.background_graphics_batch = pyglet.graphics.Batch()
        # TODO call self.idle() here instead of doing own label?
        self.window_number = window_number
        self.media_dir = 'xray'
        self.media_type = 'img'
        self.species = None
        self.serial = None
        # bdr = 10
        # rectangle = pyglet.shapes.Rectangle(
        #     bdr, bdr, self.width - (bdr * 2), self.height - (bdr * 2),
        #     color=(255, 22, 20), batch=self.background_graphics_batch)
        # rectangle.opacity = 255
        # self.background_graphics.append(rectangle)

        self.bg = pyglet.resource.image('graphics/background.png')
        # self.background_graphics.append(self.bg)
        self.bg.anchor_x = self.bg.width // 2
        self.bg.anchor_y = self.bg.height // 2

        self.label = pyglet.text.Label(
            'Please place the patient in the scanning area.',
            color=(255, 255, 255, 255),
            font_size=24, font_name='Lucida Console',
            x=self.width // 2, y=self.height // 2,
            anchor_x='center', anchor_y='center',
            batch=self.graphics_batch)
        self.graphics.append(self.label)
        self.station_label_1 = pyglet.text.Label(
            f"Station #{str(self.window_number)}",
            color=(255, 255, 255, 255),
            font_size=36, font_name='Lucida Console',
            x=125, y=self.height - 60,
            anchor_x='center', anchor_y='center',
            batch=self.graphics_batch)
        self.station_label_2 = pyglet.text.Label(
            "X-Ray",
            color=(255, 255, 255, 255),
            font_size=36, font_name='Lucida Console',
            x=125, y=60,
            anchor_x='center', anchor_y='center',
            batch=self.graphics_batch)
        # self.graphics.append(self.station_label) # keep out of batch
        self.image = None
        self.clock = pyglet.clock.get_default()
        # self.heartrate = pyglet.media.load(
        #     "media/inspiration/hrmpeg4.m4v")
        # self.heartrate_player = pyglet.media.Player()
        # self.heartrate.size = (200, 200)
        # self.heartrate_player.size = (200, 200)
        # self.heartrate_player.queue(self.heartrate)

    def idle(self, delta_time):
        """Clear medical imagery, return to idle screen."""
        self.clock.unschedule(self.idle)
        print("Going idle, ", delta_time, " seconds since scan.")
        self.clear()
        self.image = None
        self.species = None
        self.serial = None
        for graphic in self.graphics:
            graphic.delete()
        label = pyglet.text.Label(
            'Please place the patient in the scanning area.',
            color=(255, 255, 255, 255),
            font_size=24, font_name='Lucida Console',
            x=self.width // 2, y=self.height // 2,
            anchor_x='center', anchor_y='center',
            batch=self.graphics_batch)
        self.graphics.append(label)
        self.graphics_batch.draw()

    def on_tag_read(self, tag: epc.RTag | epc.FTag):
        """New tag scanned, display imagery."""
        self.clock.unschedule(self.idle)
        spec = tag.epc.species_string
        serial = tag.epc.serial
        # TODO change below line to animal/item serial
        if serial != self.serial:
            # if spec != self.species:
            print("Tag serial: ", serial)
            print("self.serial", self.serial)
            # self.clock.unschedule(self.idle)
            # TODO investigate idle after serial todo
            tag.last_seen = log.log_tag(tag)
            self.clear()
            self.serial = serial
            self.species = spec
            self.image = files.random_species_dir_type(
                spec, self.media_dir, self.media_type)
            for graphic in self.graphics:
                graphic.delete()
            species_label_1 = pyglet.text.Label(
                text="Species detected:",
                color=(255, 255, 255, 255),
                font_size=18, font_name='Lucida Console',
                x=self.width - 125, y=65,
                anchor_x='center', anchor_y='bottom',
                batch=self.graphics_batch)

            species_label_2 = pyglet.text.Label(
                text=spec.capitalize(),
                color=(255, 255, 255, 255),
                font_size=32, font_name='Lucida Console',
                x=self.width - 125, y=65,
                anchor_x='center', anchor_y='top',
                batch=self.graphics_batch)
            self.graphics.append(species_label_1)
            self.graphics.append(species_label_2)
            last_seen_date = datetime.strftime(
                tag.last_seen, "%m/%d/%Y")
            last_seen_time = datetime.strftime(
                tag.last_seen, "%H:%M:%S")
            last_seen_label_2 = pyglet.text.Label(
                text=last_seen_date,
                color=(255, 255, 255, 255),
                font_size=18, font_name='Lucida Console',
                x=self.width - 125, y=self.height - 60,
                anchor_x='center', anchor_y='center',
                batch=self.graphics_batch)
            last_seen_label_1 = pyglet.text.Label(
                text='Patient last seen:',
                color=(255, 255, 255, 255),
                font_size=16, font_name='Lucida Console',
                x=self.width - 125,
                y=self.height - 40,
                anchor_x='center', anchor_y='bottom',
                batch=self.graphics_batch)
            last_seen_label_3 = pyglet.text.Label(
                text=last_seen_time,
                color=(255, 255, 255, 255),
                font_size=18, font_name='Lucida Console',
                x=self.width - 125, y=self.height - 80,
                anchor_x='center', anchor_y='top',
                batch=self.graphics_batch)
            self.graphics.append(last_seen_label_1)
            self.graphics.append(last_seen_label_2)
            self.graphics.append(last_seen_label_3)
            self.graphics_batch.draw()
            # self.heartrate_player.play()
            self.flip()  # Required to cause window refresh
        self.clock.schedule_once(self.idle, 5)
        return pyglet.event.EVENT_HANDLED

    def on_key_press(self, symbol, modifiers):
        """Pressing any key exits app."""
        pyglet.app.exit()

    def on_draw(self):
        """Draw what should be on the screen, set by other methods."""
        self.clear()
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        if self.image:
            self.image.anchor_x = self.image.width // 2
            self.image.anchor_y = self.image.height // 2
            pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA,
                                  pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
            self.image.blit(self.width // 2, self.height // 2)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA,
                              pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        self.bg.blit(self.width // 2, self.height // 2)
        self.background_graphics_batch.draw()

        self.graphics_batch.draw()
        self.station_label_1.draw()
        self.station_label_2.draw()

        # if self.heartrate_player.texture:
        #     self.heartrate_player.texture.blit(0, 0)

    def __repr__(self):
        return f'ScannerWindow #{self.window_number}'


ScannerWindow.register_event_type('on_tag_read')


def get_video_size(width, height, sample_aspect):
    """Calculate new size based on current size and scale factor."""
    if sample_aspect > 1.:
        return width * sample_aspect, height
    if sample_aspect < 1.:
        return width, height / sample_aspect
    return width, height

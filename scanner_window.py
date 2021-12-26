#!/usr/bin/env python3
"""Subclassing pyglet Window to add behavior."""
from __future__ import annotations
from typing import List, Any
from datetime import datetime
from enum import Enum, auto
import pyglet  # type: ignore
import files
import epc
import log


class State(Enum):
    TAG_SHOWING = auto()
    IDLE = auto()


class ScannerWindow(pyglet.window.Window):
    """Subclassing pyglet Window to add logic and display."""

    def __init__(self, *args, window_number, antennas, **kwargs):
        """Set up backgroud and periphery labels."""
        super().__init__(*args, **kwargs)
        self.state = State.IDLE
        # self.background_graphics = []
        # self.graphics = []
        # self.graphics_batch = pyglet.graphics.Batch()
        # self.background_graphics_batch = pyglet.graphics.Batch()
        self.window_number = window_number
        self.media_dir = 'xray'
        self.media_type = 'img'
        self.serial = None
        self.label_controller = LabelController(self)

        self.bg = pyglet.resource.image('graphics/background.png')
        # self.background_graphics.append(self.bg)
        self.bg.anchor_x = self.bg.width // 2
        self.bg.anchor_y = self.bg.height // 2

        self.image = None
        self.clock = pyglet.clock.get_default()
        # self.heartrate = pyglet.media.load(
        #     "media/inspiration/hrmpeg4.m4v")
        # self.heartrate_player = pyglet.media.Player()
        # self.heartrate.size = (200, 200)
        # self.heartrate_player.size = (200, 200)
        # self.heartrate_player.queue(self.heartrate)
        self.idle(0)

    def idle(self, delta_time):
        """Clear medical imagery, return to idle screen."""
        self.clock.unschedule(self.idle)
        self.state = State.IDLE
        print("Going idle, ", delta_time, " seconds since scan.")
        self.clear()
        self.image = None
        self.serial = None
        self.label_controller.idle_labels.draw()

    def on_tag_read(self, tag: epc.RTag | epc.FTag):
        """New tag scanned, display imagery."""
        self.clock.unschedule(self.idle)
        self.state = State.TAG_SHOWING
        serial = tag.epc.serial
        if serial != self.serial:
            tag.last_seen = log.log_tag(tag)
            self.clear()
            self.serial = serial
            self.image = files.random_species_dir_type(
                tag.epc.species_string, self.media_dir, self.media_type)
            self.label_controller.make_tag_labels(tag).draw()
            # self.graphics_batch.draw()
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
        if self.state == State.TAG_SHOWING:
            self.label_controller.tag_labels.draw()
        elif self.state == State.IDLE:
            self.label_controller.idle_labels.draw()
        self.label_controller.always_labels.draw()
        # self.graphics_batch.draw()

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


class LabelController():
    """Manage labels for a ScannerWindow"""

    def __init__(self, window: ScannerWindow):
        """Initialize and make idle labels."""
        self.tag_labels: List[pyglet.text.Label] = []
        self.tag_graphics: List[Any] = []
        self.idle_graphics: List[Any] = []
        self.always_graphics: List[Any] = []
        self.tag_labels = pyglet.graphics.Batch()
        self.idle_labels = pyglet.graphics.Batch()
        self.always_labels = pyglet.graphics.Batch()
        self.window = window
        self.make_idle_labels()

    def idle_label_batch(self):
        """Return self.idle_label_batch"""
        return self.idle_label_batch

    def make_tag_labels(self, tag: epc.RTag | epc.FTag):
        """Delete old labels, generate new ones."""
        for item in self.tag_graphics:
            item.delete()
        self.tag_graphics = []

        # Create labels for tag:
        species_label_1 = pyglet.text.Label(
            text="Species detected:",
            color=(255, 255, 255, 255),
            font_size=18, font_name='Lucida Console',
            x=self.window.width - 125, y=65,
            anchor_x='center', anchor_y='bottom',
            batch=self.tag_labels)
        self.tag_graphics.append(species_label_1)

        species_label_2 = pyglet.text.Label(
            text=tag.epc.species_string.capitalize(),
            color=(255, 255, 255, 255),
            font_size=32, font_name='Lucida Console',
            x=self.window.width - 125, y=65,
            anchor_x='center', anchor_y='top',
            batch=self.tag_labels)
        self.tag_graphics.append(species_label_2)

        last_seen_date = datetime.strftime(
            tag.last_seen, "%m/%d/%Y")
        last_seen_time = datetime.strftime(
            tag.last_seen, "%H:%M:%S")
        last_seen_label_2 = pyglet.text.Label(
            text=last_seen_date,
            color=(255, 255, 255, 255),
            font_size=18, font_name='Lucida Console',
            x=self.window.width - 125, y=self.window.height - 60,
            anchor_x='center', anchor_y='center',
            batch=self.tag_labels)
        last_seen_label_1 = pyglet.text.Label(
            text='Patient last seen:',
            color=(255, 255, 255, 255),
            font_size=16, font_name='Lucida Console',
            x=self.window.width - 125,
            y=self.window.height - 40,
            anchor_x='center', anchor_y='bottom',
            batch=self.tag_labels)
        last_seen_label_3 = pyglet.text.Label(
            text=last_seen_time,
            color=(255, 255, 255, 255),
            font_size=18, font_name='Lucida Console',
            x=self.window.width - 125, y=self.window.height - 80,
            anchor_x='center', anchor_y='top',
            batch=self.tag_labels)
        self.tag_graphics.append(last_seen_label_1)
        self.tag_graphics.append(last_seen_label_2)
        self.tag_graphics.append(last_seen_label_3)

        return self.tag_labels

    def make_idle_labels(self):
        """Generate new idle labels."""
        label = pyglet.text.Label(
            'Please place the patient in the scanning area.',
            color=(255, 255, 255, 255),
            font_size=24, font_name='Lucida Console',
            x=self.window.width // 2, y=self.window.height // 2,
            anchor_x='center', anchor_y='center',
            batch=self.idle_labels)
        self.idle_graphics.append(label)

    def make_always_labels(self):
        station_label_1 = pyglet.text.Label(
            f"Station #{str(self.window.window_number)}",
            color=(255, 255, 255, 255),
            font_size=36, font_name='Lucida Console',
            x=125, y=self.window.height - 60,
            anchor_x='center', anchor_y='center',
            batch=self.idle_labels)
        self.always_graphics.append(station_label_1)
        station_label_2 = pyglet.text.Label(
            "X-Ray",
            color=(255, 255, 255, 255),
            font_size=36, font_name='Lucida Console',
            x=125, y=60,
            anchor_x='center', anchor_y='center',
            batch=self.idle_labels)
        self.always_graphics.append(station_label_2)
        return self.idle_labels

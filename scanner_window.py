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
    """Window state, whether a tag is being displayed."""
    IMG_SHOWING = auto()
    VID_SHOWING = auto()
    IDLE = auto()


class ScannerWindow(pyglet.window.Window):  # pylint: disable=abstract-method
    """Subclassing pyglet Window to add logic and display."""

    def __init__(self, *args, window_number, idle_seconds, ** kwargs):
        """Set up backgroud and periphery labels."""
        super().__init__(*args, **kwargs)
        self.state = State.IDLE
        # self.background_graphics = []
        # self.graphics = []
        # self.graphics_batch = pyglet.graphics.Batch()
        # self.background_graphics_batch = pyglet.graphics.Batch()
        self.window_number = window_number
        self.idle_seconds = idle_seconds
        self.media_dir = 'xray'
        self.media_type = 'img'
        self.serial = None
        self.label_controller = LabelController(self)
        self.video_player = pyglet.media.Player()
        source = pyglet.media.StreamingSource()  # TODO In pyglet examples, but unused?
        self.video_player.window = self

        @self.video_player.event  # TODO reassess after video fix
        def on_eos():  # Attempting to stop error on video end
            print("Video player telling window to idle!")
            self.idle(0)

        self.label_bg = pyglet.resource.image('graphics/background1080.png')
        # self.background_graphics.append(self.bg)
        self.label_bg.anchor_x = self.label_bg.width // 2
        self.label_bg.anchor_y = self.label_bg.height // 2

        self.image = None
        self.video = None
        self.clock = pyglet.clock.get_default()
        self.idle(0)  # idle needs delta_time argument

    def idle(self, delta_time):
        """Clear medical imagery, return to idle screen."""
        self.clock.unschedule(self.idle)
        self.state = State.IDLE
        print("Going idle, ", delta_time, " seconds since scan.")
        self.clear()
        self.image = None
        self.video = None
        self.video_player.next_source()
        self.serial = None
        self.label_controller.idle_labels.draw()

    def on_player_eos(self):  # TODO reassess after video fix
        """When video player runs out of queued files."""
        print("Player EOS received by ScannerWindow!")
        self.idle(0)

    def on_eos(self):  # TODO reassess after video fix
        """When current video file ends."""
        print("EOS received by ScannerWindow")
        self.idle(0)

    def on_tag_read(self, tag: epc.Tag):
        """New tag scanned, display imagery."""
        print("Tag received by on_tag_read in ScannerWindow")
        self.clock.unschedule(self.idle)
        serial = tag.epc.serial
        if serial != self.serial:
            tag.last_seen = log.log_tag(tag)
            self.clear()
            self.serial = serial
            print("Seeking imagery for ", tag.epc.species_string)
            if tag.epc.species_string == 'Pig':
                self.state = State.VID_SHOWING
                self.image = None
                self.video = files.random_species_dir_type(
                    'pig', 'vid', 'vid'
                )
                self.video_player.next_source()
                self.video_player.delete()
                self.video_player.queue(self.video)
                self.video_player.play()
            elif tag.epc.species_string == 'Goat':
                self.state = State.VID_SHOWING
                self.image = None
                self.video = files.random_species_dir_type(
                    'goat', 'vid', 'vid'
                )
                self.video_player.next_source()
                self.video_player.delete()
                self.video_player.queue(self.video)
                self.video_player.play()
            else:
                self.state = State.IMG_SHOWING
                self.video = None
                self.video_player.next_source()
                self.video_player.delete()
                self.image = files.random_species_dir_type(
                    tag.epc.species_string, self.media_dir, self.media_type)
                self.label_controller.make_tag_labels(tag).draw()
            # self.graphics_batch.draw()
            # self.heartrate_player.play()

            # Seemed required to cause window refresh, but caused flicker
            # self.flip() # Removed, seems to work now.
        # else:
        #     if self.state == State.VID_SHOWING:
        #         self.video_player.loop = True
        self.clock.schedule_once(self.idle, self.idle_seconds)
        return pyglet.event.EVENT_HANDLED

    def on_key_press(self, symbol, modifiers):
        """Pressing any key exits app."""
        if symbol == pyglet.window.key.P:
            print("Sending self same pig tag.")
            self.on_tag_read(epc.same_pig())
        elif symbol == pyglet.window.key.D:
            print("Sending self random dog tag.")
            self.on_tag_read(epc.random_dog())
        elif symbol == pyglet.window.key.G:
            print("Sending self same goat.")
            self.on_tag_read(epc.same_goat())
        else:
            pyglet.app.exit()

    def update(self, dt):  # TODO remove if doesn't fix video
        self.on_draw()

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
        if self.video:
            if self.video_player.source and self.video_player.source.video_format:
                self.video_player.texture.anchor_x = self.video_player.texture.width // 2
                self.video_player.texture.anchor_y = self.video_player.texture.height // 2
                self.video_player.texture.blit(
                    self.width // 2, self.height // 2)
            else:
                self.idle(0)  # TODO Figure out other return method
                # This will idle at the video end even if the animal remains.

        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA,
                              pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        if self.state != State.VID_SHOWING:
            self.label_bg.blit(self.width // 2, self.height // 2)
        if self.state == State.IMG_SHOWING:
            self.label_controller.tag_labels.draw()
        elif self.state == State.IDLE:
            self.label_controller.idle_labels.draw()
        # if self.state != State.VID_SHOWING:
        #     self.label_controller.always_labels.draw()
        # Commented out for now, as one station will show many imagery types

    def __repr__(self):
        return f'ScannerWindow #{self.window_number}'


ScannerWindow.register_event_type('on_tag_read')
ScannerWindow.register_event_type('on_player_eos')
ScannerWindow.register_event_type('on_eos')
pyglet.media.Player.register_event_type('on_eos')


def get_video_size(width, height, sample_aspect):
    """Calculate new size based on current size and scale factor."""
    if sample_aspect > 1.:
        return width * sample_aspect, height
    if sample_aspect < 1.:
        return width, height / sample_aspect
    return width, height


X_LABEL_OFFSET = 185
Y_LABEL_OFFSET = 95


class LabelController():
    """Manage labels for a ScannerWindow"""

    def __init__(self, window: ScannerWindow):
        """Initialize and make idle labels."""
        self.tag_graphics: List[Any] = []
        self.idle_graphics: List[Any] = []
        self.always_graphics: List[Any] = []
        self.tag_labels = pyglet.graphics.Batch()
        self.idle_labels = pyglet.graphics.Batch()
        self.always_labels = pyglet.graphics.Batch()
        self.window = window
        self.make_idle_labels()
        self.make_always_labels()

    def idle_label_batch(self):
        """Return self.idle_label_batch"""
        return self.idle_label_batch

    def make_tag_labels(self, tag):
        """Delete old labels, generate new ones."""
        for item in self.tag_graphics:
            item.delete()
        self.tag_graphics = []

        # Create labels for tag:
        species_label_1 = pyglet.text.Label(
            text="Species detected:",
            color=(255, 255, 255, 255),
            font_size=28, font_name='Lucida Console',
            x=self.window.width - X_LABEL_OFFSET, y=Y_LABEL_OFFSET,
            anchor_x='center', anchor_y='bottom',
            batch=self.tag_labels)
        self.tag_graphics.append(species_label_1)

        species_label_2 = pyglet.text.Label(
            text=tag.epc.species_string.capitalize(),
            color=(255, 255, 255, 255),
            font_size=48, font_name='Lucida Console',
            x=self.window.width - X_LABEL_OFFSET, y=Y_LABEL_OFFSET,
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
            font_size=28, font_name='Lucida Console',
            x=self.window.width - X_LABEL_OFFSET, y=self.window.height - Y_LABEL_OFFSET,
            anchor_x='center', anchor_y='center',
            batch=self.tag_labels)
        last_seen_label_1 = pyglet.text.Label(
            text='Patient last seen:',
            color=(255, 255, 255, 255),
            font_size=28, font_name='Lucida Console',
            x=self.window.width - X_LABEL_OFFSET,
            y=self.window.height - Y_LABEL_OFFSET + 28,
            anchor_x='center', anchor_y='bottom',
            batch=self.tag_labels)
        last_seen_label_3 = pyglet.text.Label(
            text=last_seen_time,
            color=(255, 255, 255, 255),
            font_size=28, font_name='Lucida Console',
            x=self.window.width - X_LABEL_OFFSET, y=self.window.height - Y_LABEL_OFFSET - 28,
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
            font_size=36, font_name='Lucida Console',
            x=self.window.width // 2, y=self.window.height // 2,
            anchor_x='center', anchor_y='center',
            batch=self.idle_labels)
        self.idle_graphics.append(label)

    def make_always_labels(self):
        """Create labels that will remain on screen always."""
        station_label_1 = pyglet.text.Label(
            f"Station #{str(self.window.window_number)}",
            color=(255, 255, 255, 255),
            font_size=48, font_name='Lucida Console',
            x=X_LABEL_OFFSET, y=self.window.height - Y_LABEL_OFFSET,
            anchor_x='center', anchor_y='center',
            batch=self.always_labels)
        self.always_graphics.append(station_label_1)
        station_label_2 = pyglet.text.Label(
            "X-Ray",
            color=(255, 255, 255, 255),
            font_size=48, font_name='Lucida Console',
            x=X_LABEL_OFFSET, y=Y_LABEL_OFFSET,
            anchor_x='center', anchor_y='center',
            batch=self.always_labels)
        self.always_graphics.append(station_label_2)
        return self.always_labels

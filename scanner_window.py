from __future__ import annotations
import pyglet  # type: ignore
import files
import epc
from datetime import datetime


class ScannerWindow(pyglet.window.Window):
    def __init__(self, *args, window_number, antennas, **kwargs):
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
        # bdr = 10
        # rectangle = pyglet.shapes.Rectangle(
        #     bdr, bdr, self.width - (bdr * 2), self.height - (bdr * 2),
        #     color=(255, 22, 20), batch=self.background_graphics_batch)
        # rectangle.opacity = 255
        # self.background_graphics.append(rectangle)

        self.bg = pyglet.resource.image('graphics/bg_lines.png')
        # self.background_graphics.append(self.bg)
        self.bg.anchor_x = self.bg.width // 2
        self.bg.anchor_y = self.bg.height // 2

        self.label = pyglet.text.Label('Please place the patient in the scanning area.',
                                       color=(255, 255, 255, 255),
                                       font_size=24, font_name='Gilroy',
                                       x=self.width // 2, y=self.height // 2,
                                       anchor_x='center', anchor_y='center',
                                       batch=self.graphics_batch)
        self.graphics.append(self.label)
        self.station_label = pyglet.text.Label(f"X-Ray Station #{str(self.window_number)}",
                                               color=(255, 255, 255, 255),
                                               font_size=32, font_name='Lucida Console',
                                               x=15, y=self.height - 60,
                                               anchor_x='left', anchor_y='center',
                                               batch=self.graphics_batch)
        # self.graphics.append(self.station_label) # keep out of batch to keep from delete
        self.image = None
        self.clock = pyglet.clock.get_default()
        self.heartrate = pyglet.media.load(
            "media/inspiration/hrmpeg4.m4v")
        self.heartrate_player = pyglet.media.Player()
        # self.heartrate_player.width = 200
        # self.heartrate_player.height = 200
        # self.heartrate.video_format.height = 200
        # self.heartrate.video_format.width = 200
        self.heartrate.size = (200, 200)
        self.heartrate_player.size = (200, 200)
        self.heartrate_player.queue(self.heartrate)

    def on_tag_read(self, tag: epc.rTag | epc.fTag):
        self.clock.unschedule(self.idle)
        spec = tag.species_string().lower()

        if spec != self.species:
            self.clear()
            self.species = spec
            self.image = files.random_species_dir_type(
                spec, self.media_dir, self.media_type)
            for graphic in self.graphics:
                graphic.delete()
            species_label = pyglet.text.Label(text=f'Species detected: {spec.capitalize()}',
                                              color=(255, 255, 255, 255),
                                              font_size=32, font_name='Gilroy',
                                              x=self.width - 15, y=15,
                                              anchor_x='right', anchor_y='bottom',
                                              batch=self.graphics_batch)
            self.graphics.append(species_label)
            last_seen_string = datetime.strftime(
                tag.last_seen, "%B %d, %Y at %H:%M:%S")
            last_seen_label = pyglet.text.Label(text=f'Patient last seen: {last_seen_string}',
                                                     color=(
                                                         255, 255, 255, 255),
                                                     font_size=18, font_name='Gilroy',
                                                     x=self.width - 15, y=self.height - 15,
                                                     anchor_x='right', anchor_y='top',
                                                     batch=self.graphics_batch)
            self.graphics.append(last_seen_label)
            self.graphics_batch.draw()
            # self.heartrate_player.play()
            self.flip()  # Required to cause window refresh
            self.clock.schedule_once(self.idle, 3)
        return pyglet.event.EVENT_HANDLED

    def on_key_press(self, symbol, modifiers):
        # self.clear()
        # self.flip()
        pyglet.app.exit()

    def idle(self, dt):
        self.clock.unschedule(self.idle)
        print("Going idle, ", dt, " seconds since scan.")
        self.clear()  # why was this commented out?
        self.image = None
        self.species = None
        for graphic in self.graphics:
            graphic.delete()
        label = pyglet.text.Label('Please place the patient in the scanning area.',
                                  color=(255, 255, 255, 255),
                                  font_size=24, font_name='Gilroy',
                                  x=self.width // 2, y=self.height // 2,
                                  anchor_x='center', anchor_y='center',
                                  batch=self.graphics_batch)
        self.graphics.append(label)
        self.graphics_batch.draw()

    def on_draw(self):
        self.clear()
        # pic.anchor_x = pic.width // 2
        # pic.anchor_y = pic.height // 2
        # pic.blit(x, y, z)
        self.bg.blit(self.width // 2, self.height // 2)
        self.background_graphics_batch.draw()
        if self.image:
            self.image.anchor_x = self.image.width // 2
            self.image.anchor_y = self.image.height // 2
            self.image.blit(self.width // 2, self.height // 2)
        self.graphics_batch.draw()
        self.station_label.draw()
        # if self.heartrate_player.source and self.heartrate_player.source.video_format:

        # if self.heartrate_player.texture:
        #     self.heartrate_player.texture.blit(0, 0)

    def get_video_size(width, height, sample_aspect):
        if sample_aspect > 1.:
            return width * sample_aspect, height
        elif sample_aspect < 1.:
            return width, height / sample_aspect
        else:
            return width, height


ScannerWindow.register_event_type('on_tag_read')

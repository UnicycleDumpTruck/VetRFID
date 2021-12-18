import pyglet
import files
import epc
import species
import log


class ScannerWindow(pyglet.window.Window):
    def __init__(self, *args, window_number, antennas, **kwargs):
        super().__init__(*args, **kwargs)
        # self.label_batch = pyglet.graphics.Batch()
        # TODO call self.idle() here instead of doing own label?
        self.window_number = window_number
        self.media_dir = 'xray'
        self.media_type = 'img'
        self.species = None
        self.label = pyglet.text.Label('Please place the patient in the scanning area.',
                                       color=(255, 255, 255, 255),
                                       font_size=24, font_name='Gilroy',
                                       x=self.width // 2, y=self.height // 2,
                                       anchor_x='center', anchor_y='center')
        self.station_label = pyglet.text.Label(f"Station #{str(self.window_number)}",
                                               color=(255, 255, 255, 255),
                                               font_size=24, font_name='Gilroy',
                                               x=5, y=self.height - 5,
                                               anchor_x='left', anchor_y='top')
        self.image = None
        self.clock = pyglet.clock.get_default()

    def on_tag_read(self, tag):
        self.clock.unschedule(self.idle)
        tag_string = epc.epc_to_string(tag)
        spec = species.species_str(epc.epc_species_num(tag_string)).lower()

        if spec != self.species:
            self.clear()
            self.species = spec
            self.image = files.random_species_dir_type(
                spec, self.media_dir, self.media_type)
            self.label = pyglet.text.Label(text=f'Species detected: {spec.capitalize()}',
                                           color=(255, 0, 0, 255),
                                           font_size=32, font_name='Gilroy',
                                           x=self.width - 5, y=5,
                                           anchor_x='right', anchor_y='bottom')
            self.label.draw()
            self.flip()  # Required to cause window refresh
            self.clock.schedule_once(self.idle, 1)
        return pyglet.event.EVENT_HANDLED

    def on_key_press(self, symbol, modifiers):
        self.clear()
        self.flip()
        pyglet.app.exit()

    def on_key_release(self, symbol, modifiers):
        print("Window RX Keypress")
        self.clear()
        self.image = None
        self.label = pyglet.text.Label("Keys, keys, keys!",
                                       color=(255, 0, 0, 255),
                                       x=self.width // 2, y=self.height // 2,
                                       font_size=12)
        self.label.draw()
        self.clock.schedule_once(self.idle, 2)

    def idle(self, dt):
        self.clock.unschedule(self.idle)
        print("Going idle, ", dt, " seconds since scan.")
        self.clear()  # why was this commented out?
        self.image = None
        self.species = None
        self.label = pyglet.text.Label('Please place the patient in the scanning area.',
                                       color=(255, 255, 255, 255),
                                       font_size=24, font_name='Gilroy',
                                       x=self.width // 2, y=self.height // 2,
                                       anchor_x='center', anchor_y='center')
        self.label.draw()

    def on_draw(self):
        self.clear()
        if self.image:
            self.image.blit(0, 0)
        if self.label:
            self.label.draw()
        self.station_label.draw()
        # self.label_batch.draw()
        # print("on draw label text: ", self.label.text)
        # self.flip()


ScannerWindow.register_event_type('on_tag_read')

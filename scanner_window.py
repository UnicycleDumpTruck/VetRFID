import pyglet
import files
import epc
import species
import log


class ScannerWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.label_batch = pyglet.graphics.Batch()
        # TODO call self.idle() here instead of doing own label?
        self.label = pyglet.text.Label('Please place the patient in the scanning area.',
                                       color=(255, 255, 255, 255),
                                       font_size=24,
                                       x=self.width // 2, y=self.height // 2,
                                       anchor_x='center', anchor_y='center')
        self.image = None
        self.clock = pyglet.clock.get_default()

    def on_tag_read(self, tag):
        self.clear()
        # self.image = cat
        tag_string = epc.epc_to_string(tag)
        spec = species.species_str(epc.epc_species_num(tag_string)).lower()
        media_dir = 'xray'
        media_type = 'img'
        self.image = files.random_species_dir_type(spec, media_dir, media_type)
        # print("Window Class rx epc: ", tag_string)
        # clock.schedule_once(self.label_change, 0, tag) workaround before label change worked
        self.label = pyglet.text.Label(text=spec.capitalize(),
                                       color=(255, 0, 0, 255),
                                       font_size=64,
                                       x=self.width // 2, y=self.height // 2,
                                       anchor_x='center', anchor_y='center')
        self.label.draw()

        self.flip()  # Required to cause window refresh
        return pyglet.event.EVENT_HANDLED

    def on_key_press(self, symbol, modifiers):
        self.clear()
        self.flip()

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
        self.label = pyglet.text.Label('Please place the patient in the scanning area.',
                                       color=(255, 255, 255, 255),
                                       font_size=24,
                                       x=self.width // 2, y=self.height // 2,
                                       anchor_x='center', anchor_y='center')
        self.label.draw()

    def on_draw(self):
        self.clear()
        if self.image:
            self.image.blit(0, 0)
        if self.label:
            self.label.draw()
        # self.label_batch.draw()
        # print("on draw label text: ", self.label.text)
        # self.flip()


ScannerWindow.register_event_type('on_tag_read')

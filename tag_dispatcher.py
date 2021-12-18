import pyglet
import epc


class TagDispatcher(pyglet.event.EventDispatcher):
    def __init__(self, reader, windows, antennas, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.window1 = window1
        # self.window2 = window2
        self.reader = reader
        self.clock = pyglet.clock.get_default()
        self.windows = windows
        self.antennas = antennas

    def read_tags(self, dt):
        tag_list = self.reader.read()  # TODO set timeout
        sorted_tags = {k: [] for k in self.windows.keys()}

        if tag_list:
            for tag in tag_list:
                print("Read EPC: ", epc.epc_to_string(
                    tag), ", RSSI: ", tag.rssi)
                win = self.antennas[tag.antenna]
                sorted_tags[win].append(tag)
            for window in sorted_tags:
                sorted_tags[window].sort(key=lambda tag: tag.rssi)
                best_tag = sorted_tags[window][0]
                # TODO log.log_tag(best_tag)
                best_tag_string = epc.epc_to_string(best_tag)
                print("Highest signal from read: ", best_tag_string,
                      " on antenna: ", best_tag.antenna)
                window.dispatch_event('on_tag_read', best_tag)
                print("Dispacted tag: ", best_tag_string)
                # TODO send tag to correct monitors
        else:
            # TODO Idle monitors of empty antennas.
            pass
            # self.clock.schedule_once(self.window1.idle, 1)

    def tag_read(self, tag):
        epc_string = epc.epc_to_string(tag)
        # print("Tag read: ", epc_string)
        self.window1.dispatch_event('on_tag_read', epc_string)

    def on_tag_read(self, epc):
        # I don't think we need this function
        # print("TagDispatcher Dispatched: ", epc)
        pass


TagDispatcher.register_event_type('on_tag_read')

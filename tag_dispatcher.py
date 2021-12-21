from __future__ import annotations
import pyglet  # type: ignore
import epc
import log


class TagDispatcher(pyglet.event.EventDispatcher):
    def __init__(self, reader, windows, antennas, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reader = reader
        self.clock = pyglet.clock.get_default()
        self.windows = windows
        self.antennas = antennas

    def read_tags(self, dt):
        read_tags = self.reader.read()  # TODO set timeout
        if read_tags:
            # window_tags is dict of window:[tags]
            window_tags = {k: [] for k in self.windows.keys()}

            # add tags to the appropriate list in window_tags dict
            for tag in read_tags:
                print("Read EPC: ", tag, ", RSSI: ", tag.rssi)
                win = self.antennas[str(tag.antenna)]
                window_tags[win].append(tag)

            # go thru the tags for each window, if any
            for window in window_tags:
                if window_tags[window]:
                    window_tags[window].sort(key=lambda tag: tag.rssi)
                    best_tag: epc.rTag | epc.fTag = window_tags[window][0]
                    best_tag.last_seen = log.log_tag(best_tag)
                    window.dispatch_event('on_tag_read', best_tag)
                    print("Dispacted tag: ", best_tag)


TagDispatcher.register_event_type('on_tag_read')

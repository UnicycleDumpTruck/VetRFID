"""Poll reader for new tags, send strongest read to assigned window."""
from __future__ import annotations
import pyglet  # type: ignore
import epc
import izar  # new __init__.py messing up imports?
# import log


class TagDispatcher(pyglet.event.EventDispatcher):
    """Poll reader for new tags, send strongest read to assigned window."""

    def __init__(self, reader: izar.MockReader | izar.IzarReader,
                 windows, antennas, *args, **kwargs):
        """Initialize self variables."""
        super().__init__(*args, **kwargs)
        self.reader: izar.MockReader | izar.IzarReader = reader
        self.clock = pyglet.clock.get_default()
        self.windows = windows
        self.antennas = antennas

    def read_tags(self, delta_time):
        """Poll reader for new tags, send strongest read to assigned window."""
        read_tags = self.reader.read(timeout=500)  # TODO set timeout
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
                    best_tag: epc.RTag | epc.FTag = window_tags[window][0]
                    # best_tag.last_seen = log.log_tag(best_tag)
                    window.dispatch_event('on_tag_read', best_tag)
                    print("Dispacted tag: ", best_tag)
        else:
            print("No tags detected.")


TagDispatcher.register_event_type('on_tag_read')

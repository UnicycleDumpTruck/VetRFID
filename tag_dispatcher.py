"""Poll reader for new tags, send strongest read to assigned window."""
from __future__ import annotations
from typing import Dict
from scanner_window import ScannerWindow
import pyglet  # type: ignore
import epc
import izar  # new __init__.py messing up imports?
# import log


class TagDispatcher(pyglet.event.EventDispatcher):
    """Poll reader for new tags, send strongest read to assigned window."""

    def __init__(self, reader: izar.IzarReader,
                 windows, antennas, *args, **kwargs):
        """Initialize self variables."""
        super().__init__(*args, **kwargs)
        self.reader: izar.IzarReader = reader
        self.clock = pyglet.clock.get_default()
        self.windows = windows
        self.antennas = antennas

    def read_tags(self, delta_time):
        """Poll reader for new tags, send to self.process_tags()."""
        read_tags = self.reader.read(
            timeout=500)  # TODO set timeout, argparse from main.py?
        if read_tags:
            self.process_tags(read_tags)
        else:
            print("No tags detected.")

    def tags_read(self, read_tags):
        """Called by continous read function in main.py. Processes tags if any."""
        print("Tags received from continous read: ", read_tags)
        if read_tags:
            self.process_tags(read_tags)
        else:
            raise ValueError("Empty tag list dispatched.")

    def process_tags(self, read_tags: list[epc.Tag]):
        """Send strongest tag to assigned window."""
        # window_tags is dict of window:[tag, tag, tag]
        window_tags: Dict[ScannerWindow, list[epc.Tag]] = {
            k: [] for k in self.windows.keys()}

        # add tags to the appropriate list in window_tags dict
        for tag in read_tags:
            print("Read EPC: ", tag, ", RSSI: ", tag.rssi)
            win = self.antennas[str(tag.antenna)]
            window_tags[win].append(tag)

        # go thru the tags for each window, if any
        for window in window_tags:
            if window_tags[window]:
                window_tags[window].sort(key=lambda tag: tag.rssi)
                best_tag: epc.Tag = window_tags[window][0]
                # best_tag.last_seen = log.log_tag(best_tag)
                window.dispatch_event('on_tag_read', best_tag)
                print("Dispacted tag: ", best_tag)


TagDispatcher.register_event_type('on_tag_read')

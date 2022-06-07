"""Poll reader for new tags, send strongest read to assigned window."""
from __future__ import annotations

from typing import Dict

import pyglet  # type: ignore
from loguru import logger

import epc
import izar  # new __init__.py messing up imports?
from scanner_window import ScannerWindow
import telemetry


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
        logger.debug(f"{delta_time}")
        read_tags = self.reader.read(timeout=500)
        if read_tags:
            self.process_tags(read_tags)
        else:
            print("No tags detected.")

    def tags_read(self, read_tags):
        """Called by continous read function in main.py. Processes tags if any."""
        logger.debug(f"Tags read in tag_dispatcher: {read_tags}")
        if read_tags:
            self.process_tags([epc.Tag().from_tag(read_tags)])
        else:
            raise ValueError("Empty tag list dispatched.")

    def process_tags(self, read_tags: list[epc.Tag]):
        """Send strongest tag to assigned window."""
        # window_tags is dict of window:[tag, tag, tag]
        window_tags: Dict[ScannerWindow, list[epc.Tag]] = {
            k: [] for k in self.windows.keys()}

        # add tags to the appropriate list in window_tags dict
        for tag in read_tags:
            if tag.epc.species_string:
                logger.debug(f"Sorted tag into per-window list: {tag} RSSI: {tag.rssi}")
                win = self.antennas[str(tag.antenna)]
                window_tags[win].append(tag)
            else:
                logger.warning(f"Invalid tag read: {tag.epc.code}")
                telemetry.send_log_message(f"Invalid tag read: {tag.epc.code}")
        # go thru the tags for each window, if any
        for window in window_tags:
            if window_tags[window]:
                window_tags[window].sort(key=lambda tag: tag.rssi)
                best_tag: epc.Tag = window_tags[window][0]
                # best_tag.last_seen = log.log_tag(best_tag) #TODO: Delete, not in prod?
                window.dispatch_event('on_tag_read', best_tag)
                logger.debug(f"Dispatched tag with best rssi: {best_tag}")


TagDispatcher.register_event_type('on_tag_read')

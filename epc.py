from __future__ import annotations
import species


class Tag():
    def __init__(self):
        self.epc = None
        self.antenna = None
        self.rssi = None
        self.phase = None
        self.read_count = None
        self.last_seen = None

    def serial(self):
        """Return tag serial number portion of EPC code."""
        return self.epc[0:12]

    def species_num(self):
        """Return species/animal portion of EPC code bytes or string."""
        return self.epc[12:16]

    def species_string(self):
        """Return species name as a string, like 'horse'."""
        return species.species_str(self.species_num()).lower()

    def epc_bytes(self):
        """Return epc as a bytes object."""
        return bytes(self.epc, encoding="UTF8")

    def __repr__(self):
        return str(self.epc)


class rTag(Tag):
    """Class for tags from reader hardware."""

    def __init__(self, tag):
        self.epc = str(tag.epc)
        self.phase = tag.phase
        self.antenna = tag.antenna
        self.read_count = tag.read_count
        self.rssi = tag.rssi
        self.last_seen = None


class fTag(Tag):
    """Class for fake/mock tags for testing w/o hardware."""

    def __init__(self, epc, antenna, rssi, phase, read_count):
        self.epc = epc
        self.antenna = antenna
        self.rssi = rssi
        self.phase = phase
        self.read_count = read_count
        self.last_seen = None

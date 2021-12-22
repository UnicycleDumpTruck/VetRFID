from __future__ import annotations
import species

SERIAL_DIGITS = 12
SPECIES_DIGITS = 4
DATE_FORMAT = "%Y%m%d"


class Tag():
    def __init__(self):
        self.epc = None
        self.antenna = None
        self.rssi = None
        self.phase = None
        self.read_count = None
        self.last_seen = None

    @property
    def serial(self) -> str:
        """Return tag serial number portion of EPC code."""
        return self.epc[0:12]

    @serial.setter
    def serial(self, num_str: str):
        """Set serial number portion of epc. Leading zeros will be added."""
        if not num_str.isdigit():
            raise ValueError('Serial number must be string of digits.')
        self.epc = num_str.zfill(SERIAL_DIGITS) + self.epc[SERIAL_DIGITS:]

    @property
    def species_num(self) -> str:
        """Return species/animal portion of EPC code bytes or string."""
        return self.epc[SERIAL_DIGITS:16]

    @species_num.setter
    def species_num(self, num_str: str):
        """Set species number portion of epc. Leading zeros will be added."""
        self.epc = self.epc[0:SERIAL_DIGITS] + \
            num_str.zfill(SPECIES_DIGITS) + self.epc[16:]

    @property
    def species_string(self):
        """Return species name as a string, like 'horse'."""
        return species.species_str(self.species_num()).lower()

    @property
    def epc_bytes(self):
        """Return epc as a bytes object."""
        return bytes(self.epc, encoding="UTF8")

    def __repr__(self):
        return str(self.epc)


class rTag(Tag):
    """Class for tags from reader hardware."""

    def __init__(self, tag):
        self.epc = str(tag.epc)[2:26]
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

from __future__ import annotations


class rTag():
    def __init__(self, tag):
        self.epc = str(tag.epc)
        self.phase = tag.phase
        self.antenna = tag.antenna
        self.read_count = tag.read_count
        self.rssi = tag.rssi
# TODO add methods below to rTag class


def epc_serial(epc):
    """Return tag serial number portion of EPC code."""
    return epc[0:12]


def epc_to_string(bepc):
    """Accept bytes epc or tag object, return string."""
    return str(bepc)[2:26]


def epc_species_num(epc):
    """Return species/animal portion of EPC code bytes or string."""
    return epc[12:16]


def epc_to_bytes(sepc):
    """Convert EPC string to bytes object."""
    return bytes(sepc, encoding="UTF8")

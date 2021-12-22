"""Classes to hold tags, mock/fake or scanned."""
from __future__ import annotations
from datetime import datetime
import json

# Number of digits for each field.
LOCATION_DIGITS = 4  # First four digits, location on animal
SERIAL_DIGITS = 6  # Second six, ANIMAL serial, not tag serial
SPECIES_DIGITS = 6  # Species indicator
# DATE_FORMAT = "%Y%m%d"

SERIAL_END = LOCATION_DIGITS + SERIAL_DIGITS
SPECIES_END = LOCATION_DIGITS + SERIAL_DIGITS + SPECIES_DIGITS


def json_import(filename: str) -> dict[str, str]:
    """Load species from filename, return dictionary."""
    with open(filename, 'r', encoding="UTF8") as json_file:
        data = json_file.read()
    json_dict = json.loads(data)
    return json_dict


species_names = json_import('species.json')


class EpcCode():
    """24-digit number written to Tag, containing different fields."""

    def __init__(self, code: str):
        """Initialize."""
        if code.isdigit and len(code) == 24:
            self.code: str = code
        else:
            raise ValueError("EPC should be string of 24 numerical digits.")

    @property
    def location(self) -> str:
        """Return location data string."""
        return self.code[0:LOCATION_DIGITS]

    @location.setter
    def location(self, loc: str):
        """Set location portion of EPC code."""
        if loc.isdigit and len(loc) < 5:
            self.code = "".join(
                [loc.zfill(LOCATION_DIGITS),
                 self.code[LOCATION_DIGITS:]])
            return self.code
        raise ValueError(
            "Location value should be string of four or less numerical digits.")

    @property
    def serial(self) -> str:
        return self.code[LOCATION_DIGITS:(SERIAL_END)]

    @serial.setter
    def serial(self, num_str: str):
        """Set serial number portion of epc. Leading zeros will be added."""
        if not num_str.isdigit():
            raise ValueError('Serial number must be string of digits.')
        self.code = "".join([self.location,
                            num_str.zfill(SERIAL_DIGITS),
                            self.code[SERIAL_END:]])

    @property
    def species_num(self) -> str:
        """Return species/animal portion of EPC code bytes or string."""
        return self.code[SERIAL_END:SPECIES_END]

    @species_num.setter
    def species_num(self, num_str: str) -> str:
        """Set species number portion of epc. Leading zeros will be added.
        Returns new EPC code."""
        if num_str.isdigit and len(num_str) < SPECIES_DIGITS:
            self.code = "".join([self.code[:SERIAL_END],
                                num_str.zfill(SPECIES_DIGITS),
                                self.code[SPECIES_END:]])
            return self.code
        raise ValueError(
            f"Species number must be string equal to or less than {SPECIES_DIGITS} digits.")

    @property
    def species_string(self) -> str:
        """Return species name as a string, like 'horse'."""
        spec = species_names.get(self.species_num)
        if spec:
            return spec
        raise ValueError("Species not found in species.json file.")

    @property
    def date_str(self) -> str:
        """Return date as 'YYYYMMDD'."""
        return self.code[SPECIES_END:]

    @date_str.setter
    def date_str(self, d_str: str):
        """Set date with str formated YYYYMMDD"""
        self.code = "".join([self.code[0:SPECIES_END], d_str])
        return self.code

    def date_now(self):
        """Set the date as today's date."""
        self.date_str = datetime.now().strftime("%Y%m%d")

    @property
    def epc_bytes(self):
        """Return epc as a bytes object."""
        return bytes(self.code, encoding="UTF8")

    def __repr__(self):
        return self.code


class Tag():
    """Base class for rTag and fTag."""

    def __init__(self):
        self.epc: EpcCode = None
        self.antenna = None
        self.rssi = None
        self.phase = None
        self.read_count = None
        self.last_seen = None

    # @property
    # def location(self) -> str:
    #     """Return location data string."""
    #     return self.epc.location

    # @property
    # def serial(self) -> str:
    #     """Return tag serial number portion of EPC code."""
    #     return self.epc.serial

    # @serial.setter
    # def serial(self, num_str: str):
    #     """Set serial number portion of epc. Leading zeros will be added."""
    #     self.epc.serial = num_str
    #     return self.epc

    # @property
    # def species_num(self) -> str:
    #     """Return species/animal portion of EPC code bytes or string."""
    #     return self.epc.species_num

    # @species_num.setter
    # def species_num(self, num_str: str):
    #     """Set species number portion of epc. Leading zeros will be added."""
    #     self.epc.code = num_str

    # @property
    # def species_string(self):
    #     """Return species name as a string, like 'horse'."""
    #     return self.epc.species_string

    # @property
    # def epc_bytes(self):
    #     """Return epc as a bytes object."""
    #     return bytes(self.epc, encoding="UTF8")

    def __repr__(self):
        """Represent EPC Code."""
        return str(self.epc)


class RTag(Tag):
    """Class for tags from reader hardware."""

    def __init__(self, tag):
        """Initialize."""
        self.epc = EpcCode(str(tag.epc)[2:26])
        self.phase = tag.phase
        self.antenna = tag.antenna
        self.read_count = tag.read_count
        self.rssi = tag.rssi
        self.last_seen = None


class FTag(Tag):
    """Class for fake/mock tags for testing w/o hardware."""

    def __init__(self, epc, antenna, rssi, phase, read_count):
        """Initialize."""
        self.epc = EpcCode(epc)
        self.antenna = antenna
        self.rssi = rssi
        self.phase = phase
        self.read_count = read_count
        self.last_seen = None

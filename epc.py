"""Classes to hold tags, mock/fake or scanned."""
from __future__ import annotations
from datetime import datetime
import json
from random import randint

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
    return json.loads(data)


species_names = json_import('species.json')
species_nums = {v: k for k, v in species_names.items()}


def species_name_from_int(species_num: int):
    """Given int, returns name of species."""
    return species_names.get(str(species_num).zfill(SPECIES_DIGITS))


def int_from_species_name(species_name: str) -> int:
    """Given string name of species, returns int."""
    return int(species_nums.get(species_name, default=0))


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
        return self.code[:LOCATION_DIGITS]

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
        """Return string digits of serial number, left zero padding included."""
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
    def species_num(self, num_str: str | int) -> str:
        """Set species number portion of epc. Leading zeros will be added.
        Returns new EPC code."""
        num_str = str(num_str)
        if num_str.isdigit and len(num_str) < (SPECIES_DIGITS + 1):
            self.code = "".join([self.code[:SERIAL_END],
                                num_str.zfill(SPECIES_DIGITS),
                                self.code[SPECIES_END:]])
            return self.code
        raise ValueError(
            f"Species number must be string equal to or less than {SPECIES_DIGITS} digits.")

    @property
    def species_string(self) -> str:
        """Return species name as a string, like 'horse'."""
        if spec := species_names.get(self.species_num):
            return spec
        raise ValueError("Species not found in species.json file.")

    @property
    def date_string(self) -> str:
        """Return date as 'YYYYMMDD'."""
        return self.code[SPECIES_END:]

    @date_string.setter
    def date_string(self, d_str: str):
        """Set date with str formated YYYYMMDD"""
        self.code = "".join([self.code[:SPECIES_END], d_str])
        return self.code

    def date_now(self):
        """Set the date as today's date."""
        self.date_string = datetime.now().strftime("%Y%m%d")

    @property
    def epc_bytes(self):
        """Return epc as a bytes object."""
        return bytes(self.code, encoding="UTF8")

    def __repr__(self):
        return self.code


class Tag():
    """Tag holds epc and info on the read, such as antenna and rssi."""

    def __init__(self):
        self.epc: EpcCode = None
        self.antenna = None
        self.rssi = None
        self.phase = None
        self.read_count = None
        self.last_seen = None

    def from_parameters(self, epc, antenna, rssi, phase, read_count):
        """Initialize fake/mock tag from parameters."""
        self.epc = EpcCode(epc)
        self.antenna = antenna
        self.rssi = rssi
        self.phase = phase
        self.read_count = read_count
        self.last_seen = None
        return self

    def from_tag(self, tag):
        """Initialize from hardware issued tag."""
        self.epc = EpcCode(str(tag.epc)[2:26])
        self.phase = tag.phase
        self.antenna = tag.antenna
        self.read_count = tag.read_count
        self.rssi = tag.rssi
        self.last_seen = None
        return self

    def __repr__(self):
        """Represent EPC Code."""
        return str(self.epc)


def random_dog():
    """Return a dog species tag with random serial for testing."""
    return Tag().from_parameters(
        "".join(
            '0001',
            str(randint(1, 999999)).zfill(SPECIES_DIGITS),
            '00000220211216'
        ),
        '1', '-88', '0', '1')


def random_pig():
    """Return a pig species tag with random serial for testing."""
    return Tag().from_parameters(
        "".join(
            '0001',
            str(randint(1, 999999)).zfill(SPECIES_DIGITS),
            '00000620211216'
        ),
        '1', '-88', '0', '1')


def same_pig():
    """Return a pig species tag with the same serial for testing."""
    return Tag().from_parameters(
        '0001' + '999999' + '00000620211216',
        '1', '-88', '0', '1')


def same_goat():
    """Return a pig species tag with the same serial for testing."""
    return Tag().from_parameters(
        '0001' + '888888' + '00000720211216',
        '1', '-88', '0', '1')

from datetime import datetime
import pytest
from epc import LOCATION_DIGITS, SERIAL_DIGITS, SPECIES_DIGITS, EpcCode


@pytest.fixture
def new_epc():
    new_epc = EpcCode('000000000000000000000000')
    yield new_epc


def test_init(new_epc):
    assert new_epc.code == '000000000000000000000000'


def test_location_set(new_epc):
    new_epc.location = '1' * LOCATION_DIGITS
    assert new_epc.code == ('1' * LOCATION_DIGITS) + \
        ('0' * (24 - LOCATION_DIGITS))


def test_location_get(new_epc):
    new_epc.location = '1' * LOCATION_DIGITS
    assert new_epc.location == '1' * LOCATION_DIGITS


def test_serial_set(new_epc):
    new_epc.serial = '1' * SERIAL_DIGITS
    assert new_epc.code == ('0' * LOCATION_DIGITS) + \
        ('1' * SERIAL_DIGITS) + ('0' * (SPECIES_DIGITS + 8))


def test_serial_get(new_epc):
    new_epc.serial = '1' * SERIAL_DIGITS
    assert new_epc.serial == '1' * SERIAL_DIGITS


def test_species_set(new_epc):
    new_epc.species_num = '1' * SPECIES_DIGITS
    assert new_epc.code == (
        '0' * (LOCATION_DIGITS + SERIAL_DIGITS)) + ('1' * SPECIES_DIGITS) + ('0' * 8)


def test_species_get(new_epc):
    new_epc.species_num = '1' * SPECIES_DIGITS
    assert new_epc.species_num == '1' * SPECIES_DIGITS


def test_species_horse(new_epc):
    new_epc.species_num = '1'
    assert new_epc.species_string == 'Horse'


def test_date_set(new_epc):
    new_epc.date_string = "12345678"
    assert new_epc.code == '000000000000000012345678'


def test_date_get(new_epc):
    new_epc.date_string = "12345678"
    assert new_epc.date_string == "12345678"


def test_date_now(new_epc):
    new_epc.date_now()
    now = datetime.now().strftime("%Y%m%d")
    assert new_epc.date_string == now

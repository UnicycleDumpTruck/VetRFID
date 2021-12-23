from epc import EpcCode


def test_init():
    new_epc = EpcCode('000000000000000000000000')
    assert new_epc.code == '000000000000000000000000'

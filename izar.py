"""Classes for real and mock/fake hardward reader."""
from __future__ import annotations
import mercury  # type: ignore
import epc


class IzarReader(mercury.Reader):
    """Communicates with IZAR RFID Reader."""
    # TODO Should I pass args and kwargs?

    def __init__(self, *args, **kwargs):
        """Encapsulate super init, read plan setup, print attributes."""
        super().__init__()

        print(self.get_model())
        print("Serial: ", self.get_serial())
        print("Available Antennas: ", self.get_antennas())
        print("Connected Antenna Ports: ", self.get_connected_ports())
        print("Supported Power Range in centidBm",
              self.get_power_range())

        # return self ?

    def read(self, timeout=500) -> list[epc.Tag]:
        """Return list of tags visible to reader."""
        raw_tags = super().read()
        rtag_list = [epc.Tag().from_tag(tag) for tag in raw_tags]
        return rtag_list


class MockReader():
    """Returns fake epc list on every 10th reader.read()."""

    def __init__(self, *args, **kwargs):
        """Initialize counter at zero."""
        self.counter = 0

    def read(self, timeout=500) -> list[epc.Tag]:
        """Every 10th read returns fake scans, others return empty list."""
        self.counter += 1
        if (self.counter % 10) == 0:
            # self.counter = 0
            return [
                epc.Tag().from_parameters(
                    '000211111100000120211216', '1', '-99', '0', '1'),
                epc.Tag().from_parameters(
                    '000111111200000220211216', '2', '-88', '0', '1'),
            ]
        if (self.counter % 25) == 0:
            return [
                epc.Tag().from_parameters(
                    '000111111300000620211216', '1', '-88', '0', '1'),
            ]
        return []

    def write(self, epc_code, epc_target):
        """Mock write to allow testing."""
        print(f"MockReader pretended to write {epc_code} to {epc_target}.")
        return True

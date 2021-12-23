"""Classes for real and mock/fake hardward reader."""
from __future__ import annotations
import mercury  # type: ignore
import epc


class IzarReader(mercury.Reader):
    """Communicates with IZAR RFID Reader."""

    def __init__(self, *args, **kwargs):
        """Encapsulate super init, read plan setup, print attributes."""
        super().__init__()

        print(self.get_model())
        print("Serial: ", self.get_serial())
        print("Available Antennas: ", self.get_antennas())
        print("Connected Antenna Ports: ", self.get_connected_ports())
        print("Supported Power Range in centidBm",
              self.get_power_range())

        self.set_read_plan([1, 2], "GEN2", read_power=1500)
        # return self ?

    def read(self, timeout=500) -> list[epc.RTag]:
        """Return list of tags visible to reader."""
        raw_tags = super().read()
        rtag_list = [epc.RTag(tag) for tag in raw_tags]
        return rtag_list


class MockReader():
    """Returns fake epc list on every 10th reader.read()."""

    def __init__(self, *args, **kwargs):
        """Initialize counter at zero."""
        self.counter = 0

    def read(self, timeout=500) -> list[epc.FTag]:
        """Every 10th read returns fake scans, others return empty list."""
        self.counter += 1
        if self.counter > 10:
            self.counter = 0
            return [
                epc.FTag(
                    '000211111100000120211216', '1', '-99', '0', '1'),
                epc.FTag(
                    '000111111100000220211216', '2', '-88', '0', '1'),
            ]
        return []

    def write(self, epc_code, epc_target):
        """Mock write to allow testing."""
        print(f"MockReader pretended to write {epc_code} to {epc_target}.")
        return True

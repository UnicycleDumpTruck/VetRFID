from __future__ import annotations
import mercury  # type: ignore
import epc

# class izarReader():
#     def __init__(self):
#         self.reader = mercury.Reader(
#             "llrp://izar-51e4c8.local", protocol="GEN2")
#         print(self.reader.get_model())
#         self.reader.set_read_plan([1, 2], "GEN2", read_power=1500)
#         return self.reader


class izarReader(mercury.Reader):

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

    def read(self) -> list[epc.rTag]:
        raw_tags = super().read()
        rtag_list = [epc.rTag(tag) for tag in raw_tags]
        return rtag_list


class mockReader():
    """Returns fake epc list on every 10th reader.read()."""

    def __init__(self, *args, **kwargs):
        """Initialize counter at zero."""
        self.counter = 0

    def read(self) -> list[epc.fTag]:
        """Every 10th read returns fake scans, others return empty list."""
        self.counter += 1
        if self.counter > 10:
            self.counter = 0
            return [
                epc.fTag(
                    '111111111111000120211216', '1', '-99', '0', '1'),
                epc.fTag(
                    '111111111112000220211216', '2', '-88', '0', '1'),
            ]
        else:
            return []

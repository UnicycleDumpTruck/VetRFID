import mercury
import pyglet

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


class mockReader():
    """Returns fake epc list on every 10th reader.read()."""

    def __init__(self, *args, **kwargs):
        """Initialize counter at zero."""
        self.counter = 0

    def read(self):
        """Every 10th read returns fake scans, others return empty list."""
        self.counter += 1
        if self.counter > 10:
            return [
                {'epc': b'111111111111000120211216',
                    'antenna': '1', 'rssi': '-99'},
                {'epc': b'222222222222000120211216',
                 'antenna': '2', 'rssi': '-88'},
            ]
        else:
            return []

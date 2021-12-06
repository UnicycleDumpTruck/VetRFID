#!/usr/bin/env python3
from __future__ import print_function
import time
from datetime import datetime
import mercury
reader = mercury.Reader("llrp://izar-51e4c8.local", protocol="GEN2")

print(reader.get_model())
print(reader.get_supported_regions())

reader.set_read_plan([1], "GEN2", read_power=1900) # Adding bank=["user"], causes segmentation fault
print(reader.read())

reader.start_reading(lambda tag: print(tag.epc, tag.antenna, tag.read_count, tag.rssi, datetime.fromtimestamp(tag.timestamp)))
time.sleep(10)
reader.stop_reading()

#!/usr/bin/env python3
"""Continuous read, logging each tag detected."""
from __future__ import print_function
import time
# from datetime import datetime
import mercury  # type: ignore
import log

reader = mercury.Reader("llrp://izar-51e4c8.local", protocol="GEN2")

print(reader.get_model())
print(reader.get_supported_regions())

# Adding bank= causes segmentation fault, maybe tags don't support
reader.set_read_plan([1, 2], "GEN2", read_power=1900)
# print(reader.read())

reader.start_reading(log.log_tag)
time.sleep(5)
reader.stop_reading()

#!/usr/bin/env python3
"""Read once and display list of tags detected."""
from __future__ import print_function
import mercury  # type: ignore

# reader = mercury.Reader("llrp://izar-51e4c8.local", protocol="GEN2")
reader = mercury.Reader("tmr:///dev/ttyUSB0")

print(reader.get_model())

reader.set_read_plan([1], "GEN2", read_power=1900)

print("Tags read: ", reader.read())

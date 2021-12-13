#!/usr/bin/env python3
from __future__ import print_function
import time
from datetime import datetime
import mercury
import log

reader = mercury.Reader("llrp://izar-51e4c8.local", protocol="GEN2")

print(reader.get_model())

reader.set_read_plan([1, 2], "GEN2", read_power=1900)

print("Tags read: ", reader.read())

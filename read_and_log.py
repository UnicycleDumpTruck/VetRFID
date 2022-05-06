#!/usr/bin/env python3
"""Continuous read, logging each tag detected."""
from __future__ import print_function
import time
# from datetime import datetime
import mercury  # type: ignore
import log
import epc
import datetime

def print_species_to_terminal(tag):
    e_tag = epc.Tag().from_tag(tag)
    print(e_tag.epc.species_string, "Head" if e_tag.epc.location == "0001" else "Tail", datetime.datetime.now())


reader = mercury.Reader("llrp://izar-51e4c8.local", protocol="GEN2")

print(reader.get_model())
print(reader.get_supported_regions())

# Adding bank= causes segmentation fault, maybe tags don't support
reader.set_read_plan([1, 2], "GEN2", read_power=1500)
# print(reader.read())

reader.start_reading(print_species_to_terminal)
time.sleep(600000)
reader.stop_reading()

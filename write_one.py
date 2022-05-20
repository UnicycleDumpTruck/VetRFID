#!/usr/bin/env python3
"""Most basic write for known target tag."""
from __future__ import print_function
import izar

reader = izar.IzarReader("llrp://izar-51e4c8.local", protocol="GEN2")

print(reader.get_model())
print(reader.get_supported_regions())

# Adding bank= causes segmentation fault, maybe tags don't support
# reader.set_read_plan([1, 2], "GEN2", read_power=1900)
# print(reader.read())

OLD = b'000100000800000320211223'
NEW = b'000100000800000320211223'

if reader.write(epc_code=NEW, epc_target=OLD):
    print(f"Rewrote {str(OLD)} with {str(NEW)}")
else:
    print('No tag found')
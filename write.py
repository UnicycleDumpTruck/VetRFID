#!/usr/bin/env python3
from __future__ import print_function
import mercury
reader = mercury.Reader("llrp://izar-51e4c8.local", protocol="GEN2")

print(reader.get_model())
print(reader.get_supported_regions())

reader.set_read_plan([1,2], "GEN2", read_power=1900) # Adding bank= causes segmentation fault, maybe tags don't support
#print(reader.read())

old_epc = b'000000000005000520211212'
new_epc = b'000000000005000420211212'

if reader.write(epc_code=new_epc, epc_target=old_epc):
    print('Rewrote "{}" with "{}"'.format(old_epc, new_epc))
else:
    print('No tag found')
"""Most basic write for known target tag."""
#!/usr/bin/env python3
from __future__ import print_function
import mercury  # type: ignore
reader = mercury.Reader("llrp://izar-51e4c8.local", protocol="GEN2")

print(reader.get_model())
print(reader.get_supported_regions())

# Adding bank= causes segmentation fault, maybe tags don't support
reader.set_read_plan([1], "GEN2")
# print(reader.read())

old_epc = b'000100000800000320211223'
new_epc = b'000100000700000320211223'

if reader.write(epc_code=new_epc, epc_target=old_epc):
    print(f"Rewrote {str(old_epc)} with {str(new_epc)}")
else:
    print('No tag found')

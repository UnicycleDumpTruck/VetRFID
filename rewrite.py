#!/usr/bin/env python3
"""Most basic write for known target tag."""
from __future__ import print_function
from collections import namedtuple
import time

import izar
import epc

from rich.traceback import install

install(show_locals=True)

reader = izar.IzarReader("llrp://izar-51e4c8.local", protocol="GEN2")
reader.set_read_plan([3, 4], "GEN2", read_power=1900)

print(reader.get_model())
print(reader.get_supported_regions())

EpcPair = namedtuple("EpcPair", "new old")

# tags = [TagPair(epc.Tag.from_tag(t), epc.Tag.from_tag(t))
#         for t in reader.read()]

tags = []
for tag in reader.read():
    tags.append(EpcPair(epc.EpcCode(code=str(tag)), epc.EpcCode(code=str(tag))))
    print("Added Tag to tags.")

print(f"Read tags: {tags}")
new_species = input("Enter new species name: ").strip()
new_species_num = epc.int_from_species_name(new_species)
print(f"Species looked up as {epc.species_name_from_int(new_species_num)}")

for tag_pair in tags:
    tag_pair.new.species_num = new_species_num
    print(tag_pair)
    try:
        reader.write(epc_code=tag_pair.new.epc_bytes, epc_target=tag_pair.old.epc_bytes)
        print(f"Rewrote {str(tag_pair.old)} with {str(tag_pair.new)}")
    except RuntimeError as e:
        print(f"Error, can't find tag to rewrite {tag_pair.old} with {str(tag_pair.new)}")
    time.sleep(1)

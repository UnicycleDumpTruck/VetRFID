#!/usr/bin/env python3
"""Most basic write for known target tag."""
from __future__ import print_function
from collections import namedtuple

import izar
import epc

reader = izar.IzarReader("llrp://izar-51e4c8.local", protocol="GEN2")

print(reader.get_model())
print(reader.get_supported_regions())

TagPair = namedtuple("TagPair", "new old")

tags = [TagPair(epc.Tag.from_tag(t), epc.Tag.from_tag(t))
        for t in reader.read()]

print(f"Read tags: {tags}")
new_species = input("Enter new species name: ")

for tag_pair in tags:
    tag_pair.new.epc.species_num = epc.int_from_species_name(new_species)

    if reader.write(epc_code=tag_pair.new, epc_target=tag_pair.old):
        print(f"Rewrote {str(tag_pair.old)} with {str(tag_pair.new)}")
    else:
        print(f"Error, can't find tag to rewrite {tag_pair.old}")

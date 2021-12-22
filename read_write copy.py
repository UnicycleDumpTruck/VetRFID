#!/usr/bin/env python3
from __future__ import print_function
# import time
from datetime import datetime
import mercury  # type: ignore
# import log
import species
import izar

reader = izar.mockReader()

serial_int = None
with open("last_serial.txt", 'r') as f:
    serial_int = int(f.readline().strip())

tags_read = reader.read()
print("Tags read: ", tags_read)
if tags_read:
    target_tag = tags_read[0]
    print("Targeted tag is ", target_tag)
    animal_species = None
    animal_string = None
    while True:
        animal_species = input("Enter new animal number: ")
        if animal_species.isdigit() and len(animal_species) > 5:
            animal_string = species.species_str(animal_species)
            if animal_string:
                print("Species: ", animal_string)
                break

    new_epc = str(serial_int + 1) + animal_string + \
        datetime.now().strftime("%Y%m%d")
    if len(new_epc) > 24:
        raise Exception("new_epc is too long: " + new_epc)
    if reader.write(epc_code=new_epc, epc_target=target_tag):
        print('Rewrote "{}" with "{}"'.format(target_tag, new_epc))
    else:
        print('No tag found')

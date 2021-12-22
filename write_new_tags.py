#!/usr/bin/env python3
"""Read tag, set species and write new epc."""
from __future__ import print_function
from datetime import datetime
import mercury  # type: ignore
# import log
import species
import izar

reader = izar.MockReader()

serial_int = None
with open("last_serial.txt", 'r', encoding="UTF8") as serial_file:
    serial_int = int(serial_file.readline().strip())

while input("Hit 'Return' to read & write a tag, 'n' to exit.") == "":
    tags_read = reader.read()
    print("Tags read: ", tags_read)
    if tags_read:
        # TODO set target to closest by RSSI
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
        # TODO increment serial and write back to file
        new_epc = str(serial_int + 1) + animal_string + \
            datetime.now().strftime("%Y%m%d")
        if len(new_epc) > 24:
            raise Exception(f"new_epc is too long: {new_epc}")
        if reader.write(epc_code=new_epc, epc_target=target_tag):
            print(f'Rewrote "{target_tag}" with "{new_epc}"')
        else:
            print('No tag found')

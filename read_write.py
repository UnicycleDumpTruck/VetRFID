#!/usr/bin/env python3
from __future__ import print_function
# import time
from datetime import datetime
import mercury  # type: ignore
# import log
import species

reader = mercury.Reader("llrp://izar-51e4c8.local", protocol="GEN2")

print(reader.get_model())

reader.set_read_plan([1], "GEN2", read_power=1900)

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
        animal_species = input("Enter new animal number: ").zfill(4)
        print(f"Entered: {animal_species}")
        if animal_species.isdigit():
            animal_string = species.species_str(animal_species.zfill(4))
            print(f"animal_string: {animal_string}")
            if animal_string:
                print("Species: ", animal_string)
                break

    new_epc = bytes((str((serial_int + 1)).zfill(12) + animal_species + \
        datetime.now().strftime("%Y%m%d")), encoding='UTF8')
    if len(new_epc) > 27:
        raise Exception("new_epc is too long: " + new_epc)
    #reader.write(epc_code=new_epc, epc_target=target_tag)
    print('Rewrote "{}" with "{}"'.format(target_tag, new_epc))
    #else:
    #    print('No tag found')

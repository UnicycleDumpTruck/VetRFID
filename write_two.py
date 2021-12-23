#!/usr/bin/env python3
"""Read and write tags in sets of two per item/animal number."""
from __future__ import print_function
# import log
import izar
import epc
from time import sleep


# reader = izar.MockReader()
reader = izar.IzarReader("llrp://izar-51e4c8.local", protocol="GEN2")
# reader.set_read_plan([1], "GEN2", read_power=1500)
# reader.set_read_plan([1], "GEN2", read_power=1900)
reader.set_read_plan([1], "GEN2")

NUM_TAGS_PER_SERIAL = 2
location = 1

serial_int = None
with open("last_serial.txt", 'r', encoding="UTF8") as serial_file:
    serial_int = int(serial_file.readline().strip())

def increment_serial(s_int):
    if s_int is None:
        raise ValueError("Serial number can't be None.")
    s_int += 1
    with open('last_serial.txt', 'w', encoding='UTF8') as serial_file:
        serial_file.write(str(s_int))
    return s_int


while True: # input("Hit 'Return' to continue, 'n' then 'Return' to exit.") == "":
    # Set species for session
    species = input("Enter new animal number: ").strip()
    location = 1

    while input("'Return' to continue, 'n' then 'Return' for new species:") == "":
        tags_read = reader.read(timeout=100)
        sleep(0.5)
        print("Tags read: ", tags_read)
        if tags_read:
            # TODO set target to closest by RSSI
            target_tag = tags_read[0]
            print("Targeted tag", target_tag)
            new_epc = epc.EpcCode("000000000000000000000000")
            new_epc.species_num = species
            print("Species: ", new_epc.species_string)
            new_epc.serial = str(serial_int + 1)
            new_epc.location = str(location)
            new_epc.date_now()
            if len(new_epc.code) > 24:
                raise ValueError(f"new_epc is too long: {new_epc}")
            old = target_tag.epc.epc_bytes
            new = new_epc.epc_bytes
            if reader.write(epc_code=new, epc_target=old):
                print(f'Rewrote {old}\nwith    {new}')
                location += 1
                if location > 2:
                    serial_int = increment_serial(serial_int)
                    location = 1
            else:
                print('No tag found')

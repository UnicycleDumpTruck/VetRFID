#!/usr/bin/env python3
"""Read tag, set species and write new epc."""
from __future__ import print_function
# import log
import izar
import epc

# reader = izar.MockReader()
reader = izar.IzarReader('llrp://izar-51e4c8.local', protocol="GEN2")


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
        new_epc = epc.EpcCode("000000000000000000000000")
        new_epc.species_num = input("Enter new animal number: ").strip()
        print("Species: ", new_epc.species_string)
        new_epc.serial = str(serial_int + 1)
        new_epc.location = input("Tag location digits (max 4):").strip()
        new_epc.date_now()
        if len(new_epc.code) > 24:
            raise Exception(f"new_epc is too long: {new_epc}")
        print(new_epc.epc_bytes)
        if reader.write(epc_code=new_epc.epc_bytes, epc_target=target_tag.epc.epc_bytes):
            print(f'Rewrote "{target_tag}"\nwith    "{new_epc.code}"')
            # print(f'Readable version: {readable_epc}')
            serial_int += 1
            with open('last_serial.txt', 'w', encoding='UTF8') as serial_file:
                serial_file.write(str(serial_int))
        else:
            print('No tag found')
        # TODO increment serial and write back to file

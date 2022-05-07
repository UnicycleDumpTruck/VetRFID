#!/usr/bin/env python3
"""Read and write tags in sets of two per item/animal number."""
from __future__ import print_function
from time import sleep
import izar
import epc


# reader = izar.MockReader()
reader = izar.IzarReader("llrp://izar-51e4c8.local", protocol="GEN2")
# reader.set_read_plan([1], "GEN2", read_power=1500)
# reader.set_read_plan([1], "GEN2", read_power=1900)
reader.set_read_plan([1], "GEN2")

NUM_TAGS_PER_SERIAL = 2

serial_int: int
with open("last_serial.txt", 'r', encoding="UTF8") as serial_file_in:
    serial_int = int(serial_file_in.readline().strip())


def increment_serial(s_int):
    """Given an integer, write it to file tracking last serial number used."""
    if s_int is None:
        raise ValueError("Serial number can't be None.")
    s_int += 1
    with open('last_serial.txt', 'w', encoding='UTF8') as serial_file_out:
        serial_file_out.write(str(s_int))
    return s_int


# input("Hit 'Return' to continue, 'n' then 'Return' to exit.") == "":
while True:
    # Set species for session
    species = input("Enter new animal number: ").strip()
    tag_position: int = 1  # pylint: disable=invalid-name

    while input(f"'Return' to write {epc.species_name_from_int(int(species))} {tag_position}") == "":
        tags_read = reader.read(timeout=100)
        sleep(0.5)
        print("Tags read: ", tags_read)
        if tags_read:
            # TODO set target to closest by RSSI
            target_tag = tags_read[0]
            # print("Targeted tag", target_tag)
            new_epc = epc.EpcCode("000000000000000000000000")
            new_epc.species_num = species
            new_epc.serial = str(serial_int + 1)
            new_epc.location = str(tag_position)
            new_epc.date_now()
            if len(new_epc.code) > 24:
                raise ValueError(f"new_epc is too long: {new_epc}")
            old = target_tag.epc.epc_bytes
            new = new_epc.epc_bytes
            if reader.write(epc_code=new, epc_target=old):
                print(f'Rewrote {old}\nwith    {new}')
                print("Label your tag:", new_epc.species_string, end=", ")
                print("Head" if tag_position == 1 else "Tail", end=", ")
                print(serial_int + 1)

                # Increment counters after successful write
                tag_position += 1
                if tag_position > 2:
                    serial_int = increment_serial(serial_int)
                    tag_position = 1  # pylint: disable=invalid-name

            else:
                print('No tag found')

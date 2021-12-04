# VetRFID
Museum exhibit using a JADAK 4-port RFID reader to read laundry tags in plush animals and display pretend medical imagery.

- Currently exploring read functions in exploration.py
- Test table of animal short names and pretty names in species.csv
- tag_log will hold TID, first_seen, last_seen, num_reads
- Folders of sounds and folder of images. Short names will match tag, sound, image.

# TODO
- Indefinite reading, stop_read on exception or exit?
- Set up Pyglet, test multiple monitors.
- Investigate multiple monitors on RPi.
- Investitate multi-channel sound on RPi. 3+ channels?
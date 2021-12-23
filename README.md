# VetRFID

Museum exhibit using a JADAK 4-port RFID reader to read laundry tags in plush animals and display pretend medical imagery.

## Files and folders

- main.py is the main application for the exhibit
- write_new_tags.py is for setting up new RFID tags
- tag_log.csv will hold EPC, first_seen, last_seen, num_reads
- species.json holds animal names and numbers
- last_serial.txt tracks last tag serial number written
- Folders of sounds and folder of images. Short names will match tag, sound, image.

## TODO

- Fix background on fullscreen multiple monitors.
- Investitate multi-channel sound.
- Experiment with antenna placement, shielding, & power
- Setup.py
- Better test coverage, where possible

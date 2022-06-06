# VetRFID

Museum exhibit component in a vet-themed exhibit, using a
JADAK 4-port RFID reader to read laundry tags in plush
animals and display pretend medical imagery. Software runs
two monitors on an Ubuntu desktop computer with NVidia 1660.

## Files and folders

- main.py is the main application for the exhibit
- write_gui.py is for setting up new RFID tags
- jlog.json holds EPC, first_seen, last_seen, num_reads
- species.json holds animal species names and associated numbers
- last_serial.txt tracks last tag serial number written
- media/all contains imagery displayed
- media/overlays are species-specific labels overlayed on imagery

## TODO

- Species Changer gui application for changing species of multiple tags
- Setup.py
- Better test coverage, where possible given GUI

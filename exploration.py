#!/usr/bin/env python3
from __future__ import print_function
import time
from datetime import datetime
import mercury

def exeception_handle(e):
    print("Uh-oh! Exception handler called!")
    print(e)

def print_tag(tag):
    print(  "EPC: ", tag.epc, 
            "Ant: ", tag.antenna, 
            "Count: ", tag.read_count, 
            "RSSI: ", tag.rssi, 
            "Time: ", datetime.fromtimestamp(tag.timestamp),
            "User: ", tag.user_mem_data
        )

print("Marbles RFID Scanning Station")

reader = mercury.Reader("llrp://izar-51e4c8.local")

reader.enable_exception_handler(exeception_handle)

print("Reader Model: ", reader.get_model())
print("Software Version: ", reader.get_sofware_version())
print("Serial: ", reader.get_serial())
print("Available Antennas: ", reader.get_antennas())
print("Connected Antenna Ports: ", reader.get_connected_ports())
print("Supported Power Range in centidBm", reader.get_power_range())

reader.set_read_plan([1], "GEN2", read_power=1900)
print(reader.read())

# reader.start_reading(callback, on_time=250, off_time=0)
reader.start_reading(lambda tag: print( "EPC: ", tag.epc, 
                                        "Ant: ", tag.antenna, 
                                        "RSSI: ", tag.rssi, 
                                        "Time: ", datetime.fromtimestamp(tag.timestamp),
                                        ))
time.sleep(10)
reader.stop_reading()

print("Testing new read with print_tag function and on_time, off_time...")
reader.start_reading(print_tag, on_time=250, off_time=0)
time.sleep(10)
reader.stop_reading()

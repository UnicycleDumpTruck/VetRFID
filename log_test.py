#!/usr/bin/env python3
from __future__ import print_function
import time
from datetime import datetime
import mercury
import pandas as pd
reader = mercury.Reader("llrp://izar-51e4c8.local", protocol="GEN2")

def log_tag(tag):
    current_time = datetime.now()
    print("Read: ", tag.epc, tag.antenna, tag.read_count, tag.rssi)
    print("Log before reading: ")
    df = pd.read_csv('tag_log.csv')
    #df.set_index('epc')
    print(df.to_string())
    if not (df.loc[df['epc'] == str(tag.epc)].empty):
        print("Row found")
        df.loc[df['epc'] == str(tag.epc), 'last_seen'] = current_time
        previous_num_reads = df.loc[df['epc'] == str(tag.epc)][0]['num_reads']
        print("num_reads", previous_num_reads)
        df.loc[df['epc'] == str(tag.epc), 'last_seen'] = current_time
    else:
        df.loc[len(df.index)] = [tag.epc, tag.epc[12:16], current_time, current_time, previous_num_reads + 1]
    print("Dataframe after:\n", df.to_string())
    df.to_csv('tag_log.csv', index=False) #, index=False

reader.set_read_plan([1,2], "GEN2", read_power=1900) # Adding bank= causes segmentation fault, maybe tags don't support
# print(reader.read())

reader.start_reading(log_tag)
time.sleep(1)
reader.stop_reading()

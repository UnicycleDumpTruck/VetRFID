import pandas as pd
from datetime import datetime
import csv
import json

log_format = {
    "100000000000000000000000":{'species': 'horse', 'first_seen':str(datetime.now()), 'last_seen':str(datetime.now()), 'num_reads':'0'},
    "100000000000000000000001":{'species': 'horse', 'first_seen':str(datetime.now()), 'last_seen':str(datetime.now()), 'num_reads':'0'},
    "100000000000000000000002":{'species': 'horse', 'first_seen':str(datetime.now()), 'last_seen':str(datetime.now()), 'num_reads':'0'},
}


def epc_serial(epc):
    # Return tag serial number portion of EPC code
    return epc[0:12]


def epc_species_num(epc):
    return epc[13:16]


def epc_to_string(bepc):
    return str(epcb)[2:26]


def epc_to_bytes(sepc):
    return bytes(sepc, encoding="UTF8")


def old_log_tag(tag):
    current_time = datetime.now()
    print("Read: ", tag.epc, tag.antenna, tag.read_count, tag.rssi)
    print("Log before reading: ")
    df = pd.read_csv('tag_log.csv')
    # df.set_index('epc')
    print(df.to_string())
    if not (df.loc[df['epc'] == str(tag.epc)].empty):
        print("Row found")
        df.loc[df['epc'] == str(tag.epc), 'last_seen'] = current_time
        #previous_num_reads = df.loc[df['epc'] == str(tag.epc)][0]['num_reads']
        #print("num_reads", previous_num_reads)
        #df.loc[df['epc'] == str(tag.epc), 'last_seen'] = current_time
    else:
        df.loc[len(df.index)] = [tag.epc, tag.epc[12:16],
                                 current_time, current_time, 0]
    print("Dataframe after:\n", df.to_string())
    df.to_csv('tag_log.csv', index=False)  # , index=False

def json_import(filename):
    with open(filename, 'r') as f:
        data = f.read()
    js = json.loads(data)
    return js

def json_export(filename, ldict):
    with open(filename, 'w') as f:
        jstr = json.dumps(ldict)
        f.write(jstr)



epcb = bytes("000000000001000120211207", encoding="UTF8")

#log_epc(epcb)

log_dict = json_import('jlog.txt')
for itm in log_dict.items():
    print(itm)
log_dict['100000000000000000000000']['species'] = "cat"
json_export('jlog.txt', log_dict)

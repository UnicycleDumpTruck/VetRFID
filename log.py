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

def epc_to_string(bepc):
    return str(bepc)[2:26]

def epc_species_num(epc):
    return epc[12:16]


def epc_to_bytes(sepc):
    return bytes(sepc, encoding="UTF8")


def json_import(filename):
    with open(filename, 'r') as f:
        data = f.read()
    js = json.loads(data)
    return js

def json_export(filename, ldict):
    with open(filename, 'w') as f:
        jstr = json.dumps(ldict)
        f.write(jstr)

def print_log_dict(ldict):
    for itm in ldict.items():
        print(itm[0], itm[1].values())


def log_epc(epc): # string input
    log_dict = json_import('jlog.txt')
    if log_dict.get(epc):
        #print(epc)
        log_dict[epc]['last_seen'] = str(datetime.now())
        log_dict[epc]['num_reads'] = str(int(log_dict[epc]['num_reads']) + 1)
    else:
        log_dict[epc] =  { 'species':epc_species_str(epc), 
                                'first_seen':str(datetime.now()),
                                'last_seen':str(datetime.now()),
                                'num_reads':'1',
                                }
    #log_dict['100000000000000000000000']['species'] = "cat"
    json_export('jlog.txt', log_dict)

def log_tag(tag):
    string_epc = epc_to_string(tag.epc)
    log_epc(string_epc)
    print("Logged: ", string_epc)

# log_epc("000000000001000120211207")
# log_epc("000000000001000120211208")
# log_epc("000000000001000120211209")

species_dict = json_import('species.json')


def epc_species_str(epc):
    return species_dict[epc_species_num(epc)]

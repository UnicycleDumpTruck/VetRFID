from datetime import datetime
import csv
import json
import files
import epc
import species

# log_format = {
#     "100000000000000000000000":{'species': 'horse', 'first_seen':str(datetime.now()), 'last_seen':str(datetime.now()), 'num_reads':'0'},
#     "100000000000000000000001":{'species': 'horse', 'first_seen':str(datetime.now()), 'last_seen':str(datetime.now()), 'num_reads':'0'},
#     "100000000000000000000002":{'species': 'horse', 'first_seen':str(datetime.now()), 'last_seen':str(datetime.now()), 'num_reads':'0'},
# }


def print_log_dict(ldict):
    for itm in ldict.items():
        print(itm[0], itm[1].values())


def log_epc(epc): # string input
    log_dict = files.json_import('jlog.json')
    if log_dict.get(epc):
        #print(epc)
        log_dict[epc]['last_seen'] = str(datetime.now())
        log_dict[epc]['num_reads'] = str(int(log_dict[epc]['num_reads']) + 1)
    else:
        log_dict[epc] =  { 'species':epc.epc_species_str(epc), 
                                'first_seen':str(datetime.now()),
                                'last_seen':str(datetime.now()),
                                'num_reads':'1',
                                }
    files.json_export('jlog.json', log_dict)


def log_tag(tag):
    string_epc = epc.epc_to_string(tag.epc)
    log_epc(string_epc)
    print("Logged: ", string_epc)



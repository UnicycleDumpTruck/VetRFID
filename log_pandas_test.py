import pandas as pd
from datetime import datetime


def epc_serial(epc):
    return epc[0:12]


def epc_species_num(epc):
    return epc[13:16]


def epc_to_string(bepc):
    return str(epcb)[2:26]


def epc_to_bytes(sepc):
    return bytes(sepc, encoding="UTF8")


def log_tag(tag):
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


def log_epc(epc):
    df = pd.read_csv('tag_log.csv')
    print(df.to_string())
    idx = df.index[df['epc'] == str(epc)]
    reads = int(df.iloc[idx]['num_reads'].values[0]) + 1
    print(reads)
    df.loc[idx]['last_seen'] = datetime.now()
    df.loc[idx]['num_reads'] = reads
    print(df.to_string())
    df.to_csv('tag_log.csv', index=False)  # , index=False


epcb = bytes("000000000001000120211207", encoding="UTF8")
# print(epcb)
# print(str(epcb)[2:26])

log_epc(epcb)

from datetime import datetime
import pandas as pd


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
        previous_num_reads = df.loc[df['epc'] == str(tag.epc)][0]['num_reads']
        print("num_reads", previous_num_reads)
        df.loc[df['epc'] == str(tag.epc), 'last_seen'] = current_time
    else:
        df.loc[len(df.index)] = [tag.epc, tag.epc[12:16],
                                 current_time, current_time, previous_num_reads + 1]
    print("Dataframe after:\n", df.to_string())
    df.to_csv('tag_log.csv', index=False)  # , index=False

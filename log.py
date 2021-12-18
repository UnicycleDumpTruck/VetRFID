from __future__ import annotations
from datetime import datetime
import files
import epc

log_format = {
    "100000000000000000000000": {'species': 'horse', 'first_seen': str(datetime.now()), 'last_seen': str(datetime.now()), 'num_reads': '0'},
    "100000000000000000000001": {'species': 'horse', 'first_seen': str(datetime.now()), 'last_seen': str(datetime.now()), 'num_reads': '0'},
    "100000000000000000000002": {'species': 'horse', 'first_seen': str(datetime.now()), 'last_seen': str(datetime.now()), 'num_reads': '0'},
}


def print_log_dict(ldict):
    """Print dictionary line by line."""
    for itm in ldict.items():
        print(itm[0], itm[1].values())


def log_tag(tag: epc.rTag | epc.fTag) -> datetime:  # string input
    """Log epc string to jlog.json file."""
    log_dict = files.json_import('jlog.json')
    last_seen = None
    if log_dict.get(tag.epc):
        print(f"Logged: {tag.epc}")
        last_seen = log_dict[tag.epc]['last_seen']
        last_seen_obj = datetime.strptime(last_seen, "%Y-%m-%d %H:%M:%S.%f")
        last_seen_str = datetime.strftime(last_seen_obj, "%m/%d/%Y, %H:%M:%S")
        print(f"Tag last seen {last_seen_str}")
        log_dict[tag.epc]['last_seen'] = str(datetime.now())
        log_dict[tag.epc]['num_reads'] = str(
            int(log_dict[tag.epc]['num_reads']) + 1)
        log_dict[tag.epc]['species'] = tag.species_string()
    else:
        log_dict[tag.epc] = {'species': tag.species_string(),
                             'first_seen': str(datetime.now()),
                             'last_seen': str(datetime.now()),
                             'num_reads': '1',
                             }
    files.json_export('jlog.json', log_dict)
    return last_seen_obj


# def log_tag(tag):
#     """Get string of epc from tag and send it to log_epc function for jlog.json."""
#     string_epc = epc.epc_to_string(tag.epc)
#     log_epc(string_epc)
#     print("Logged: ", string_epc)

# files.json_export('jlog.json', log_format)

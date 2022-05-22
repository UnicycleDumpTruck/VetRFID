"""Log tags to file for popularity tracking."""
from __future__ import annotations
from datetime import datetime
import files
import epc

# If the jlog.json file gets wiped, put an empty pair
# of {} in it to allow a new file to be created.

# TODO: If no log file exists, create it.
# TODO: Put log filename in constant, rename to end in ".log"


def print_log_dict(ldict):
    """Print dictionary line by line."""
    for itm in ldict.items():
        print(itm[0], itm[1].values())


def log_tag(tag: epc.Tag) -> datetime:
    """Log epc string to jlog.json file."""
    log_dict = files.json_import('jlog.json')
    last_seen = None
    last_seen_obj = None
    if log_dict.get(tag.epc.code):
        last_seen = log_dict[tag.epc.code]['last_seen']
        last_seen_obj = datetime.strptime(last_seen, "%Y-%m-%d %H:%M:%S.%f")
        last_seen_str = datetime.strftime(last_seen_obj, "%m/%d/%Y, %H:%M:%S")
        print(f"Logged {tag.epc.code}. Last seen {last_seen_str}")
        log_dict[tag.epc.code]['last_seen'] = str(datetime.now())
        log_dict[tag.epc.code]['num_reads'] = str(
            int(log_dict[tag.epc.code]['num_reads']) + 1)
        log_dict[tag.epc.code]['species'] = tag.epc.species_string
    else:
        log_dict[tag.epc.code] = {'species': tag.epc.species_string,
                                  'first_seen': str(datetime.now()),
                                  'last_seen': str(datetime.now()),
                                  'num_reads': '1',
                                  }
        last_seen_obj = datetime.now()
    files.json_export('jlog.json', log_dict)
    return last_seen_obj

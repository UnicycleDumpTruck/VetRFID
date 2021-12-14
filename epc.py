# Functions to parse EPC codes

def epc_serial(epc):
    # Return tag serial number portion of EPC code
    return epc[0:12]


def epc_to_string(bepc):
    return str(bepc)[2:26]


def epc_species_num(epc):
    return epc[12:16]


def epc_to_bytes(sepc):
    return bytes(sepc, encoding="UTF8")
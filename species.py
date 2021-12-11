# Functions to load dictionary of species numbers and names
# from json file, and function to return name for a species number

import json

def json_import(filename):
    with open(filename, 'r') as f:
        data = f.read()
    js = json.loads(data)
    return js


def species_str(species_num):
    return species_names[species_num]


species_names = json_import('species.json')
print("Species Loaded: ", species_names)

for num in range(1, len(species_names)+1):
    num_str = str(num).zfill(4)
    print(num_str, species_names[num_str])

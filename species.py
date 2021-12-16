# Functions to load dictionary of species numbers and names
# from json file, and function to return name for a species number
from __future__ import annotations
import json


def json_import(filename: str) -> dict[str, str]:
    """Load species from filename, return dictionary."""
    with open(filename, 'r') as f:
        data = f.read()
    js = json.loads(data)
    return js


def species_str(species_num: str) -> str | None:
    """Lookup species number in loaded dictionary, return animal name string."""
    return species_names.get(species_num)


species_names = json_import('species.json')
print("Species Loaded: ", species_names)

for num in range(1, len(species_names) + 1):
    num_str = str(num).zfill(4)
    print(num_str, species_names[num_str])

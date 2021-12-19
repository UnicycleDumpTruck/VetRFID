import json
import pyglet  # type: ignore
import os
import random


def json_import(filename):
    """Read json from 'filename', return dictionary."""
    with open(filename, 'r') as f:
        data = f.read()
    js = json.loads(data)
    return js


def json_export(filename, ldict):
    """Write dictionary to filename as json."""
    with open(filename, 'w') as f:
        jstr = json.dumps(ldict, indent=4, sort_keys=True)
        f.write(jstr)


file_types = {'img': pyglet.resource.image, }


def random_species_dir_type(animal_species, media_directory, media_type):
    """Given species, directory, media type, return random pyglet.resource.

    Args:
        animal_species ([string]): ["monkey"]
        media_directory ([string]): ["xray"]
        media_type ([string]): ["img"]

    Returns:
        [pyglet.resource....]: [resource type determined by media_type]
    """
    # animal_species="monkey", media_directory="xray"
    p = "media/" + animal_species + "/" + media_directory + "/"
    f = file_types[media_type](p + random.choice(os.listdir(p)))

    # may not work for images larger than 1280 x 720...
    if media_type == 'img':
        scale_factor = f.height / 720
        f.height = 720
        f.width = f.width / scale_factor

    return f

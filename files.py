"""Load dict from json file. Make random pyglet imag from directory."""
import json
import os
import random
import pyglet  # type: ignore


def json_import(filename):
    """Read json from 'filename', return dictionary."""
    with open(filename, 'r', encoding="UTF8") as json_file:
        data = json_file.read()
    js = json.loads(data)
    return js


def json_export(filename, ldict):
    """Write dictionary to filename as json."""
    with open(filename, 'w', encoding="UTF8") as json_file:
        jstr = json.dumps(ldict, indent=4, sort_keys=True)
        json_file.write(jstr)


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
    dir_path = "media/" + animal_species.lower() + "/" + media_directory + "/"
    img_resource = file_types[media_type](
        dir_path + random.choice(os.listdir(dir_path)))

    # may not work for images larger than 1280 x 720...
    if media_type == 'img':
        scale_factor = img_resource.height / 720
        img_resource.height = 720
        img_resource.width = img_resource.width / scale_factor

    return img_resource

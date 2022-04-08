"""Load dict from json file. Make random pyglet imag from directory."""
import json
import os
import random
import copy
import pyglet  # type: ignore
from rich.traceback import install
install(show_locals=True)


def json_import(filename) -> dict:
    """Read json from 'filename', return dictionary."""
    with open(filename, 'r', encoding="UTF8") as json_file:
        data = json_file.read()
    js_dict = json.loads(data)
    return js_dict


def json_export(filename, ldict):
    """Write dictionary to filename as json."""
    with open(filename, 'w', encoding="UTF8") as json_file:
        jstr = json.dumps(ldict, indent=4, sort_keys=True)
        json_file.write(jstr)


file_types = {'img': pyglet.resource.image, 'vid': pyglet.media.load, }


def random_species_dir_type(animal_species, media_directory, media_type):
    """Given species, directory, media type, return random pyglet.resource.

    Args:
        animal_species ([string]): "monkey", "dog", or "pig"
        media_directory ([string]): "xray"
        media_type ([string]): "img" or "vid"

    Returns:
        [pyglet.resource....]: [resource type determined by media_type]
    """
    # animal_species="monkey", media_directory="xray"
    dir_path = "media/" + animal_species.lower() + "/" + media_directory + "/"
    all_files = os.listdir(dir_path)
    valid_files = []
    for file in all_files:
        if file[0] != ".":
            valid_files.append(file)
    print(valid_files)
    img_path = dir_path + random.choice(valid_files)
    print(img_path)
    img_resource = file_types[media_type](img_path)

    orig_image = img_resource
    if media_type == 'img':
        orig_image = copy.copy(img_resource)

        height, width = 1080, 1920  # Desired resolution

        scale_y = min(img_resource.height, height) / \
            max(img_resource.height, height)
        scale_x = min(width, img_resource.width) / \
            max(width, img_resource.width)
        img_resource.scale = min(scale_x, scale_y)

        img_resource.width = img_resource.width * img_resource.scale
        img_resource.height = img_resource.height * img_resource.scale

    # may not work for images larger than 1920 x 1080...
    # if media_type == 'img':
    #     scale_factor = img_resource.height / 1080
    #     img_resource.height = 1080
    #     img_resource.width = img_resource.width / scale_factor

    # TODO: Video scaling
    # elif media_type == 'vid':
    #     scale_factor = img_resource.size.height / 1080
    #     img_resource.size.height = 1080
    #     img_resource.size.width = img_resource.size.width / scale_factor

    return img_resource, orig_image

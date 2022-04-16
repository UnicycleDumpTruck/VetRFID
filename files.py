"""Load dict from json file. Make random pyglet imag from directory."""
from __future__ import annotations
from typing import List
import json
import os
import random
import copy
from PIL import Image
import pyglet  # type: ignore
from loguru import logger
from rich.traceback import install
install(show_locals=True)


def json_import(filename) -> dict:
    """Read json from 'filename', return dictionary."""
    with open(filename, 'r', encoding="UTF8") as json_file:
        data = json_file.read()
    return json.loads(data)


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
    dir_path = f"media/{animal_species.lower()}/{media_directory}/"
    all_files = os.listdir(dir_path)
    valid_files = [file for file in all_files if file[0] != "."]
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

new_ext = {".jpg": ".png", "jpeg": "png", "webp": "png"}

def convert_all_to_png():
    logger.info("Printing file list.")
    for dirpath, dirnames, files in os.walk('media'):
        logger.info(f"Directory: {dirpath}")
        for file_name in files:
            logger.info(file_name)
            logger.info(file_name[-4:])
            if file_name[-4:] in {".jpg", "jpeg", "webp"}:
                new_name = os.path.join(dirpath, f"{file_name[:-4]}{new_ext[file_name[-4:]]}")
                old_name = os.path.join(dirpath, file_name)
                logger.info(new_name)
                if not os.path.isfile(new_name):
                    try:
                        with Image.open(old_name) as other_type_file:
                            other_type_file.save(new_name)
                        
                    except Exception as e:
                        logger.error(e)
                else:
                    os.remove(old_name)


def list_all_png() -> List:
    file_list = []
    for dirpath, dirnames, files in os.walk('media'):
        for file_name in files:
            file_path = os.path.join(dirpath, file_name)
            logger.info(file_path)
            file_list.append(file_path)
    return file_list

if __name__ == "__main__":
    list_all_png()
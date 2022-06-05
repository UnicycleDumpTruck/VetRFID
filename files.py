"""Load dict from json file. Make random pyglet imag from directory.
Image conversion functions.
"""
from __future__ import annotations
from typing import List
import json
import os
import random
import copy
from glob import glob
from PIL import Image
import pyglet  # type: ignore
from loguru import logger
from rich.traceback import install

import log

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


file_types = {'img': pyglet.resource.image,
              # 'vid': pyglet.resource.image, }
              'vid': pyglet.media.load, }


def random_of_species(species: str):
    """Given species, return random pyglet.resource.

    Args:
        species ([string]): "monkey", "dog", or "pig"

    Returns:
        [pyglet.resource....]: [resource type determined by media_type]
        [string]: file type, either "img" or "vid"
    """
    species = species.replace(" ", "_").lower()
    # logger.info(f"Looking for {species} files")
    glob_path = f"media/all/*{species}*"
    if species_glob := glob(glob_path):
        file_path = random.choice(species_glob)
        log.log_file(file_path)
        if file_path[-4:] == ".mp4":
            file_type = "vid"
        elif file_path[-4:] in {"jpeg", ".jpg", ".png"}:
            file_type = "img"
        else:
            raise ValueError(
                "Unable to match file extension to determine file_type.")
        resource = file_types[file_type](file_path)
        if overlay_glob := glob(f"media/species_overlays/*{species}*"):
            overlay = pyglet.resource.image(random.choice(overlay_glob))
        else:
            logger.warning(
                f"No overlay found for {species}, returned overlay=None")
            overlay = None
        return resource, file_type, overlay
    logger.warning(f"No files found for {species}!")
    return None, None, None


def rand_ext_of_species(ext, species):
    """Given file extension (without period) and species name,
    return random file of that extension."""
    glob_path = f"media/all_{ext}/*{species}*"
    if species_glob := glob(glob_path):
        return random.choice(species_glob)
    return None


def scale_image(img):
    """Scale image to 1920 by 1080"""
    height, width = 1080, 1920  # Desired resolution
    # height, width = 720, 1280  # Desired resolution

    scale_y = min(img.height, height) / max(img.height, height)
    scale_x = min(width, img.width) / max(width, img.width)

    if img.height < height and img.width < width:
        img.scale = max(scale_x, scale_y)
        img.width = img.width / img.scale
        img.height = img.height / img.scale
    else:
        img.scale = min(scale_x, scale_y)
        img.width = img.width * img.scale
        img.height = img.height * img.scale

    return img  # TODO: not necessary, since scaled in place. remove and test.


# Extension replacements for use converting new files:
new_ext = {".jpg": ".png", "jpeg": "png", "webp": "png"}


def convert_all_to_png():
    logger.info("Printing file list.")
    for dirpath, dirnames, files in os.walk('media'):
        logger.info(f"Directory: {dirpath}")
        for file_name in files:
            logger.info(file_name)
            logger.info(file_name[-4:])
            if file_name[-4:] in {".jpg", "jpeg", "webp"}:
                new_name = os.path.join(
                    dirpath, f"{file_name[:-4]}{new_ext[file_name[-4:]]}")
                old_name = os.path.join(dirpath, file_name)
                logger.info(new_name)
                if not os.path.isfile(new_name):
                    try:
                        with Image.open(old_name) as other_type_file:
                            other_type_file.save(new_name)

                    except Exception as e:
                        logger.warning(e)
                else:
                    os.remove(old_name)


def list_all_of(file_extension: str) -> List:
    file_list = []
    for dirpath, dirnames, files in os.walk('media'):
        for file_name in files:
            if file_name.endswith(file_extension) and not file_name.endswith("."):
                file_path = os.path.join(dirpath, file_name)
                # logger.info(file_path)
                file_list.append(file_path)
    return file_list


# TODO: Enclose following into slideshow class?

all_png = list_all_of("png")
current_png = 0
all_mp4 = list_all_of("mp4")
current_mp4 = 0


def next_png():
    global current_png
    current_png += 1
    if current_png >= len(all_png):
        current_png = 0
    return load_png(all_png[current_png])


def prev_png():
    global current_png
    current_png -= 1
    if current_png < 0:
        current_png = len(all_png) - 1
    return load_png(all_png[current_png])


def load_png(path):
    logger.debug(path)
    resource = pyglet.resource.image(path)
    orig = copy.copy(resource)
    return scale_image(resource), orig


def load_mp4(path):
    logger.debug(f"Loading MP4: {path}")
    return pyglet.media.load(path)


def next_mp4():
    global current_mp4
    current_mp4 += 1
    if current_mp4 >= len(all_mp4):
        current_mp4 = 0
    return load_mp4(all_mp4[current_mp4])


def prev_mp4():
    global current_mp4
    current_mp4 -= 1
    if current_mp4 < 0:
        current_mp4 = len(all_mp4) - 1
    return load_mp4(all_mp4[current_mp4])


if __name__ == "__main__":
    for _ in range(20):
        print(rand_ext_of_species("png", "snake"))
        print(rand_ext_of_species("png", "turtle"))

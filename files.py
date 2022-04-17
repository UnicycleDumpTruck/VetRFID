"""Load dict from json file. Make random pyglet imag from directory."""
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

    orig_image = copy.copy(img_resource)
    if media_type == 'img':
        return scale_image(img_resource), orig_image

    # TODO: Video Scaling
    return img_resource, orig_image  # TODO: toss extra return, clean from SWin


def rand_of_species(ext, species):
    glob_path = f"/media/all_{ext}/{species}*"
    species_glob = glob(glob_path)
    return random.choice(species_glob)


def scale_image(img):
    # height, width = 1080, 1920  # Desired resolution
    height, width = 720, 1280  # Desired resolution

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

    return img


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
                        logger.error(e)
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
        print(rand_of_species("turtle"))

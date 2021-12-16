import json
import species
import pyglet
import os
import random


def json_import(filename):
    with open(filename, 'r') as f:
        data = f.read()
    js = json.loads(data)
    return js


def json_export(filename, ldict):
    with open(filename, 'w') as f:
        jstr = json.dumps(ldict)
        f.write(jstr)


file_types = {'img': pyglet.resource.image, }


def random_species_dir_type(animal_species, media_directory, media_type):
    # animal_species="monkey", media_directory="xray"
    p = "media/" + animal_species + "/" + media_directory + "/"
    f = file_types[media_type](p + random.choice(os.listdir(p)))
    return f

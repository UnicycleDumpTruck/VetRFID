"""Test loading of files."""
from os import path, listdir
# import pytest
import pyglet  # type: ignore

# working_dir = os.path.dirname(os.path.realpath(__file__))
two_up = path.abspath(path.join(__file__, "../../.."))
MEDIA_DIR = path.join(two_up, 'media')
all_species_dirs = [path.join(MEDIA_DIR, dirname, "xray/")
                    for dirname in listdir(MEDIA_DIR)
                    if dirname[0] != "."]
print(all_species_dirs)


# pyglet.resource.path = []
# pyglet.resource.reindex()

def test_load_one_xray():
    img = pyglet.image.load(path.abspath(
        path.join(MEDIA_DIR, 'cat/xray/001.jpg')))
    assert isinstance(img, pyglet.image.ImageData)


def test_load_every_xray():
    """Test load every xray image."""
    for species_dir in all_species_dirs:
        files = [f"{species_dir}{filename}"
                 for filename in listdir(species_dir)
                 if filename[0] != "."]
        print(files)
        for file in files:
            img = pyglet.image.load(path.abspath(file))
            print(f"Loaded {type(img)} of size {img.width}, {img.height}")
            assert isinstance(img, pyglet.image.ImageData)

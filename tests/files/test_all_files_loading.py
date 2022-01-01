"""Test loading of files."""
import os
import pytest
import pyglet  # type: ignore

#working_dir = os.path.dirname(os.path.realpath(__file__))
MEDIA_DIR = os.path.join('media')
all_species_dirs = [os.path.join(MEDIA_DIR, dirname, "xray/")
                    for dirname in os.listdir(MEDIA_DIR)
                    if dirname[0] != "."]
print(all_species_dirs)


pyglet.resource.path = []
pyglet.resource.reindex()


def test_load_every_xray():
    """Test load every xray image."""
    for species_dir in all_species_dirs:
        files = [f"{species_dir}{filename}"
                 for filename in os.listdir(species_dir)
                 if filename[0] != "."]
        print(files)
        for file in files:
            img = pyglet.image.load(os.path.abspath(file))
            print(f"Loaded {type(img)} of size {img.width}, {img.height}")
            assert isinstance(img, pyglet.image.ImageData)

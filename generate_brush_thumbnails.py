"""
Takes a list of .kpp paintoppreset files, generates thumbnails
with PIL, and saves them as .kpp krita paintoppresets
"""
import os
import tkinter as tk
from tkinter import filedialog
import codecs
import csv
from PIL import Image, PngImagePlugin

from distutils.dir_util import copy_tree
from subprocess import Popen

# -------
# OPTIONS
# -------
ASSETS_FOLDER = os.path.realpath("thumbnails-assets")
SAVE_FOLDER = os.path.realpath("dist")
USE_SRC_FOLDER = True
OPTIMIZE = True


# ---------
# FUNCTIONS
# ---------
def get_brush_parameters(file_path):
    """Generator that yields brush file data from a CSV file"""
    with codecs.open(csv_file_path, 'r', 'utf-8-sig') as data:
        csv_iterable = csv.reader(data)
        header = next(csv_iterable)
        for row in csv_iterable:
            brush = dict(zip(header, row))
            yield brush


def create_thumbnail(base, *args):
    """
    returns a thumbnail Image
    Uses Image.alpha_composite to generate the thumbnail image
    using any amount of layers. *args must be PIL images
    """
    composite = base
    for layer in args:
        if layer is None:
            continue
        if layer.size != composite.size:
            layer = layer.crop(composite.getbbox())
        if layer.mode != composite.mode:
            layer = layer.convert(mode=composite.mode)
        composite = Image.alpha_composite(composite, layer)
    return composite


def get_brush_metadata(image):
    """
    Takes a PIL Image object and returns a PngInfo object
    that contains the file's metadata to override pnginfo
    on save.
    """
    metadata = PngImagePlugin.PngInfo()
    for key, value in image.info.items():
        if key not in RESERVED:
            metadata.add_text(key, value, 0)
    return metadata

# ------
# SCRIPT
# ------
# Get the paths of files that contains the thumbnails and csv data
tk.Tk().withdraw()
start_folder = './src' if USE_SRC_FOLDER else filedialog.askdirectory(
).replace('/', '\\')
file_names = [f for f in os.listdir(start_folder)]

# Get the CSV
csv_file_path = next(os.path.join(start_folder, name)
                     for name in file_names if name.endswith('.csv'))
brush_names = [name[:-4] for name in file_names if name.endswith('.kpp')]
brush_paths = {name: os.path.join(start_folder, name + ".kpp")
               for name in brush_names}

if not csv_file_path:
    raise AttributeError('Missing CSV file')
if not brush_names:
    raise AttributeError('No paintoppreset found (.kpp files)')

# Store the presets' data from the CSV
brush_data = []
for brush in get_brush_parameters(file_path=csv_file_path):
    for name in brush_names:
        if name == brush['NAME']:
            brush['FILE'] = name
            brush_data.append(brush)

# Preload all sprites to compose the final thumbnail
assets = {}
for directory in os.listdir(ASSETS_FOLDER):
    directory_path = ASSETS_FOLDER + "\\" + directory
    assets[directory] = {}
    for asset in os.listdir(directory_path):
        if asset.endswith('.png'):
            assets[directory][asset[:-4]] = Image.open(directory_path + "\\" +
                                                       asset)

if not os.path.exists(SAVE_FOLDER):
    os.mkdir(SAVE_FOLDER)

# Process each file based on CSV data
brushes_count = len(brush_data)
progress = 0
RESERVED = ('interlace', 'gamma', 'dpi', 'transparency', 'aspect')
for brush in brush_data:
    brush_metadata = None
    brush_name = brush['FILE']
    if brush_name in brush_paths.keys():
        with Image.open(brush_paths[brush_name]) as source:
            brush_metadata = get_brush_metadata(image=source)
    if not brush_metadata:
        print('Metadata not found for {!s}, couldn\'t create thumbnail'.format(brush_name))
        continue

    xml_data = brush_metadata.chunks
    base = assets['base'][brush['BASE']]
    outline = assets['outline'][brush['OUTLINE']]
    try:
        stroke = assets['stroke'][brush['NAME']]
    except:
        stroke = None
    try:
        pictogram = assets['pictogram'][brush['PICTOGRAM']]
    except:
        pictogram = None
    thumbnail = create_thumbnail(base, stroke, outline, pictogram)

    filename = brush['NAME'] + ".kpp"
    thumbnail.save(
        os.path.join(SAVE_FOLDER, filename),
        format='png',
        pnginfo=brush_metadata,
        optimize=OPTIMIZE)

    progress += 1
    print("\rProgress: {!s}/{!s}".format(progress, brushes_count),
          end="",
          flush=True)


# TODO: Copy thumbs to Krita presets folder for testing
# krita_preset_folder = r'C:\Users\natlo_000\AppData\Roaming\krita\paintoppresets'
# copy_tree(output_presets, krita_preset_folder)
# Popen(['explorer', krita_preset_folder])

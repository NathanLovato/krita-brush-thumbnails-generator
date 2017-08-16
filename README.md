# Krita brushes thumbnail generator

Krita brush presets take time to create. On top of the brush settings, you have to draw your own thumbnails one by one, which adds to the workload. You'll likely reuse backgrounds and pictograms. Editing existing thumbnails can be time-consuming too. As your brush set grows, you'll likely have to redesign some older presets as well. 

That's what this brush thumbnail generator is for. It takes some sprites, Krita brush presets, CSV data and generates new brush thumbnails.

## How to use

### The sprites

All sprites should be the same size! Krita uses 200px * 200px pictures for its presets' thumbnails.

Each thumbnail has up to 4 layers:

1. The base, or its background
2. The stroke
3. The outline
4. The pictogram

The tool comes with demo assets. Feel free to use them to design your own brushes, and run the script to see how it works (see below).

### CSV data

The CSV file needs to be encoded as utf-8, and the data comma delimited.

Keep the header in the file, and fill each row with:

1. NAME: the preset's filename without the extension
2. TYPE (_optional_): the brush engine you use ; not used by the script
3. PACK (_optional_): to sort all your presets if you produce several bundles
4. PICTOGRAM: the pictogram's filename without the extension
5. OUTLINE: the outline's filename without the extension
6. BASE: the base's filename without the extension

### Prerequisites

Python 3 with the Pillow image library installed.

If you use pip to install python packages, in the command line, type:

```shell
$ pip install Pillow
```

See the full install guide on [Pillow's documentation](http://pillow.readthedocs.io/en/4.0.x/installation.html)

### The source presets

Place the CSV file and the source brush presets in the /src folder.

To pick a different source folder, edit the generate_brush_thumbnails.py file. Change `USE_SRC_FOLDER` to `False`. A file picker will pop up and let you choose another directory.

### Run the script

Open a shell in the brush generator's folder, and run

```shell
$ python generate_brush_thumbnails.py
```

Within a few seconds, it'll generate the brush presets. The script will overwrite files in the /dist folder, if any.


## License

All the code and png files in this repository are available under the MIT license. Other files are only present for demo purposes, and not available to distribute.

Copyright 2017 Nathan Lovato (GDquest)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

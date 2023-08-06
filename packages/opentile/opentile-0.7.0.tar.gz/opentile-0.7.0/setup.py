# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opentile']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.1,<10.0.0',
 'PyTurboJPEG>=1.6.1,<2.0.0',
 'imagecodecs>=2022.12.24,<2023.0.0',
 'numpy>=1.22.0,<2.0.0',
 'tifffile>=2022.5.4,<2023.0.0']

setup_kwargs = {
    'name': 'opentile',
    'version': '0.7.0',
    'description': 'Read tiles from wsi-TIFF files',
    'long_description': "# *opentile*\n\n*opentile* is a Python library for reading tiles from wsi tiff files. The aims of the proect are:\n\n- Allow compressed tiles to be losslessly read from wsi tiffs using 2D coordinates (tile position x, y).\n- Provide unified interface for relevant metadata.\n- Support all file formats supported by tifffile that has a non-overlapping tile structure.\n\nCrrently supported file formats are listed and described under *Supported file formats*.\n\n## Installing *opentile*\n\n*opentile* is available on PyPI:\n\n```console\npip install opentile\n```\n\n## Important note\n\nPlease note that this is an early release and the API is not frozen yet. Function names and functionality is prone to change.\n\n## Requirements\n\n*opentile* requires python >=3.8 and uses numpy, Pillow, TiffFile, and PyTurboJPEG (with lib-turbojpeg >= 2.1 ).\n\n## Limitations\n\nFiles with z-stacks are currently not fully supported for all formats.\n\n## Supported file formats\n\nThe following description of the workings of the supported file formats does not include the additional specifics for each format that is handled by tifffile. Additional formats supported by tifffile and that have non-overlapping tile layout are likely to be added in future release.\n\n***Hamamatsu Ndpi***\nThe Ndpi-format uses non-rectangular tile size typically 8 pixels high, i.e. stripes. To form tiles, first multiple stripes are concatenated to form a frame covering the tile region. Second, if the stripes are longer than the tile width, the tile is croped out of the frame. The concatenation and crop transformations are performed losslessly.\n\nA ndpi-file can also contain non-tiled images. If these are part of a pyramidal series, *opentile* tiles the image.\n\nThe macro page in ndpi-files images the whole slide including label. A label and overview is created by cropping the macro image.\n\n***Philips tiff***\nThe Philips tiff-format allows tiles to be sparse, i.e. missing. For such tiles, *opentile* instead provides a blank (currently white) tile image using the same jpeg header as the rest of the image.\n\n***Aperio svs***\nSome Asperio svs-files have corrupt tile data at edges of non-base pyramidal levels. This is observed as tiles with 0-byte length and tiles with incorrect pixel data. *opentile* detects such corruption and instead returns downscaled image data from lower levels. Associated images (label, overview) are currently not handled correctly.\n\n***3DHistech tiff***\nOnly the pyramidal levels are supported (not overviews or labels).\n\n## Metadata\n\nFile metadata can be accessed through the `metadata`-property of a tiler. Depending on file format and content, the following metadata is avaiable:\n\n- Magnification\n- Scanner manufacturer\n- Scanner model\n- Scanner software versions\n- Scanner serial number\n- Aquisition datetime\n\n## Basic usage\n\n***Load a Ndpi-file using tile size (1024, 1024) pixels.***\n\n```python\nfrom opentile import OpenTile\ntile_size = (1024, 1024)\nturbo_path = 'C:/libjpeg-turbo64/bin/turbojpeg.dll'\ntiler = OpenTile.open(path_to_ndpi_file, tile_size, turbo_path)\n```\n\n***Get rectangular tile at level 0 and position x=0, y=0.***\n\n```python\ntile = tiler.get_tile(0, (0, 0))\n```\n\n***Close the tiler object.***\n\n```python\ntiler.close()\n```\n\n***Usage as context manager***\n\nThe tiler can also be used as context manager:\n\n```python\nfrom opentile import OpenTile\ntile_size = (1024, 1024)\nturbo_path = 'C:/libjpeg-turbo64/bin/turbojpeg.dll'\nwith OpenTile.open(path_to_ndpi_file, tile_size, turbo_path) as tiler:\n    tile = tiler.get_tile(0, (0, 0))\n```\n\n## Setup environment for development\n\nRequires poetry and pytest and pytest-watch installed in the virtual environment.\n\n```console\ngit clone https://github.com/imi-bigpicture/opentile.git\npoetry install\n```\n\nBy default the tests looks for slides in 'tests/testdata'. This can be overriden by setting the OPENTILE_TESTDIR environment variable. The script 'tests/download_test_images.py' can be used to download publically available [openslide testdata](https://openslide.cs.cmu.edu/download/openslide-testdata/) into the set testdata folder:\n\n```console\npython tests/download_test_images.py\n```\n\nThe test data used for philips tiff is currently not publically available as we dont have permission to share them. If you have slides in philips tiff format that can be freely shared we would be happy to use them instead.\n\nTo watch unit tests use:\n\n```console\npoetry run pytest-watch -- -m unittest\n```\n\n## Other TIFF python tools\n\n- [tifffile](https://github.com/cgohlke/tifffile)\n- [tiffslide](https://github.com/bayer-science-for-a-better-life/tiffslide)\n\n## Contributing\n\nWe welcome any contributions to help improve this tool for the WSI community!\n\nWe recommend first creating an issue before creating potential contributions to check that the contribution is in line with the goals of the project. To submit your contribution, please issue a pull request on the imi-bigpicture/opentile repository with your changes for review.\n\nOur aim is to provide constructive and positive code reviews for all submissions. The project relies on gradual typing and roughly follows PEP8. However, we are not dogmatic. Most important is that the code is easy to read and understand.\n\n## Acknowledgement\n\n*opentile*: Copyright 2021 Sectra AB, licensed under Apache 2.0.\n\nThis project is part of a project that has received funding from the Innovative Medicines Initiative 2 Joint Undertaking under grant agreement No 945358. This Joint Undertaking receives support from the European Union’s Horizon 2020 research and innovation programme and EFPIA. IMI website: www.imi.europa.eu\n",
    'author': 'Erik O Gabrielsson',
    'author_email': 'erik.o.gabrielsson@sectra.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/imi-bigpicture/opentile',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)

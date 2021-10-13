from distutils.core import setup
from glob import glob
import py2exe, os

py2exe_options = dict(
    optimize=2,
    compressed=True,
    bundle_files=1,
    dist_dir='release',
    )

setup(
    data_files = [('resources', glob('resources/*.*'))],
    options ={'py2exe': py2exe_options},
    windows = [{'script': "BlockDropGame.py"}],
    zipfile=None,
)

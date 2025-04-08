import os
import shutil
from setuptools import setup, Extension
from Cython.Build import cythonize

# Build the extension
setup(
    ext_modules=cythonize([
        Extension(
            "decoder", 
            ["other/decoder.py"],
        )
    ])
)

# After building, find and rename the file
for file in os.listdir('.'):
    if file.startswith('decoder') and (file.endswith('.so') or '.so.' in file):
        shutil.move(file, 'decoder.so')
        print(f"Created decoder.so from {file}")
        break
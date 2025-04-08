#!/usr/bin/env python3
from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        name="decoderLib",           # nazwa modułu
        sources=["decoder.py"],   # źródło – używamy pliku decoder.py (może być kompilowany przez Cython)
        language="c",             # język C (Cython generuje kod C)
    )
]

setup(
    name="decoderLib",
    ext_modules=cythonize(extensions, language_level="3"),
)

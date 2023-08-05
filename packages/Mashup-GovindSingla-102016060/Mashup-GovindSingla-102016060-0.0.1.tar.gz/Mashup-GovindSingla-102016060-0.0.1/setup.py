from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'This module will create a mashup sort of thing of any singer you want of any duration with just simple command.'

# Setting up
setup(
    name="Mashup-GovindSingla-102016060",
    version=VERSION,
    author="Govind Singla",
    author_email="<gsingla_be20@thapar.edu>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[           
          'pytube',
          'pydub',
      ],
    keywords = ['MASHUP', 'YOUTUBE', 'PROJECT','MUSIC','MP3'], 
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

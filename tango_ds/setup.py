#!/usr/bin/env python3

# Imports
from setuptools import setup

# Setup
setup(name="tangods-raspberry_pi",
      version="0.1.0",
      packages=['raspberry_pi'],
      entry_points={
          'console_scripts': ['RaspberryPiIO = raspberry_pi:run']},
      zip_safe=False,
      license="GPLv3",
      description="Tango device server for the Raspberry Pi.",

      author="Sundberg",
      author_email="jens.sundberg@maxiv.lu.se",
      url="http://www.maxiv.lu.se",
      install_requires=['setuptools', 'pytango>=9.2.1'],
      tests_require=['pytest', 'pytest-xdist'],
      setup_requires=['pytest-runner']
      )

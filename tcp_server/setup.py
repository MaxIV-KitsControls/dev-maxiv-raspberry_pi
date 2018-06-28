#!/usr/bin/env python3

# Imports
from setuptools import setup

# Setup
setup(name="tcpserver-raspberry_pi",
      version="0.1.0",
      py_modules = ['rpi_gpio_server', 'advanced_streamer'],
      entry_points={
          'console_scripts': ['tcpserver-raspberry_pi = rpi_gpio_server:main']},
      zip_safe=False,
      license="GPLv3",
      description="TCP server for the Raspberry Pi Tango device.",

      author="J. Sundberg, A. Dupre, J. Murari",
      author_email="jens.sundberg@maxiv.lu.se, antoine.dupre@maxiv.lu.se, juliano.murari@maxiv.lu.se",
      url="http://www.maxiv.lu.se",
      install_requires=['setuptools'],
      )

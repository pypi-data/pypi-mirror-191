"""
CCDfits
=======

Provides
  1. A simple way to view and analyze .fits images that were obtained with CCDs
  2. Algorithms to process images originated in Skipper CCDs

This package requires that `astropy`, `numpy`, `matplotlib` and `scipy` 
be installed within the Python environment.

Available modules
---------------------
classes
	defines FITS and CCD objects
processing
	Skipper CCD image processing tools
utilities
	Analysis tools for image-like arrays
"""

from .classes import Fits, maskedFits, CCD


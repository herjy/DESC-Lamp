# standard python imports
import numpy as np
import os
import scipy
import astropy.io.fits as pyfits
import scipy.ndimage
import matplotlib.pyplot as plt
import imageio
from mpl_toolkits.axes_grid1 import make_axes_locatable

# lenstronomy utility functions
import lenstronomy.Util.util as util
import lenstronomy.Util.image_util as image_util

import galsim

def Lensed_source(Cutout):
    """ Object to described lensed sources"""
    def __init__(self, gsobject, spectrum):
        
    def from_gso(image, wcs = None, pix = None):
        """ Declares a Lensed source from an image.
        Parameters
        ----------
        image: array
            image of a galaxy to use in as a source for lensing.
        wcs: WCS
            wcs of the image
        pix: float
            size of the pixels in `image` in arcseconds 
        
        """
        if pix is None: 
            assert wcs is not None
            
        
        gsobject = galsim.InterpolatedImage(galsim.Image(image_high_res_lensed), scale = pix)
        
        
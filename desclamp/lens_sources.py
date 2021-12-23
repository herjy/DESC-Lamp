# standard python imports
import numpy as np
import matplotlib.pyplot as plt

# lenstronomy utility functions
import lenstronomy.Util.util as util
import lenstronomy.Util.image_util as image_util

import galsim

def Lensed_source(Cutout):
    """ Object to described lensed sources"""
    def __init__(self, gsobject, spectrum):
        self.spectrum = spectrum
        self.gso = gsobject
        
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
            
        
        gsobject = galsim.InterpolatedImage(galsim.Image(self.gso), scale = pix)
        
        
# standard python imports
import numpy as np
import matplotlib.pyplot as plt

# lenstronomy utility functions
import lenstronomy.Util.util as util
import lenstronomy.Util.image_util as image_util
from lenstronomy.ImSim.image_model import ImageModel
from lenstronomy.LensModel.lens_model import LensModel
from lenstronomy.LightModel.light_model import LightModel
from lenstronomy.Data.imaging_data import ImageData
import lenstronomy.Util.simulation_util as sim_util

import galsim


class Lensed_source:
    """ Object to described lensed sources"""
    def __init__(self, spectrum, image = None, shape=(100,100), shift=(0,0), pix = 0.2, wcs = None):
        """
        Source object that carries source and lens information and generates lensed source images for injection.
        Parameters
        ----------
        gsobject: `galsim.GSObject`
            a galsim representation for the source galaxy
        spectrum: array
            An array that contains the spectrum (colour) of the source.
        shape: `tuple`
            Shape of the source galaxy patch in source plane
        shift: tuple
            shifts the source object in its patch. Default is (0,0): centered in the patch.
        pix: `float`
            pixel size in arcseconds. Default id Rubin's pixel.
        wcs: WCS
            wcs information for the source patch. 
        
        """
        if pix is None: 
            assert wcs is not None
            try:
                model_affine = wcs.wcs.pc
            except AttributeError:
                model_affine = wcs.cd
                
            pix = np.sqrt(np.abs(model_affine[0, 0])* np.abs(model_affine[1, 1] - model_affine[0, 1] * model_affine[1, 0]))
            
        self.pix = pix
        self.shift = shit
        self.image = image
        self.shape = shape
        self.spectrum = spectrum
        if self.image is not None:
            self.source_image = self.draw_source()
    
    def lens_source(self, lens_models, hr_factor, **kwargs):
        assert self.image is not None, "Please provide a source image."

        kwargs_data_high_res = sim_util.data_configure_simple(slef.shape*hr_factor, self.pix/hr_factor)
        data_high_res = ImageData(**kwargs_data_high_res)
        
        lensModel = LensModel(lens_models)
        sourceLightModel = LightModel(['INTERPOL'])
 
        kwargs_lens
        kwargs_source
        
        imageModel_high_res = ImageModel(data_class=data_high_res, lens_model_class=lensModel, source_model_class=sourceLightModel)
        lensed_image = imageModel_high_res.image(kwargs, kwargs_source, kwargs_lens_light=None, kwargs_ps=None)
        return lensed_image
    
    def draw_source(self):
        """ Draws a soource no a grid specified by the parameters of the __init__
        """
        x, y = util.make_grid(numPix=self.shape, deltapix=1.)
        kwargs_list = [
            {'image': self.image, 'scale': 1, 'phi_G': 0, 'center_x': self.shift[0], 'center_y': self.shift[1]}
        ]
        lightModel = LightModel(light_model_list=['INTERPOL'])
        return lightModel.surface_brightness(x, y, kwargs_list)
    
    @property
    def image(self):
        return self.image
    
    @image.setter
    def image(self, image):
        self.image = image
        self.source_image = self.draw_source()
    
    def from_gsobject(self, gsobject, smooth=0):
        """ Creates a Lensed source from a galsim object.
        Parameters
        ----------
        gsobject: Galsim Object
            image of a galaxy to use in as a source for lensing.
        smooth: bool
            Value of the sigma for a gaussian smoothing kernel. Useful to apply if the input image is noisy or contains sharp features.
        """
        if smooth > 0:
            gso = galsim.Convolve(gsobject, galsim.Gaussian(sigma=smooth))
        #Draws the galsim object on a grid    
        source = gso.drawImage(nx=shape[0],
            ny=shape[1],
            use_true_center = True,
            method='real_space',
            scale=self.pix,
            dtype=np.float64).array
        self.image(source)
        return self
        
    def from_lenstronomy(self, kwargs):
        """TO DO"""
        pass
    
    @staticmethod
    def from_galsim_parametric(profile='Sersic', **kwargs):
        """ Creates a Lensed source object from a source described as a parametric profile.
        Parameters
        ----------
        spectrum: array
            The spectrum of the the source
        profile: string
            The galsim profile to use to generate a source galaxy. Currently, Sersic, DeVeaucouleurs and Exponential are implemented
        kwargs:
            parameters of the profile
            
        Returns
        -------
        A `Lensed_source` object.
        """
        
        assert profile in ['Sersic', 'Exponential', 'DeVeaucouleurs'], "Not a valid profile. Please use 'Sersic', 'Exponential' or 'DeVeaucouleurs'."
        
        if profile == 'Sersic':
            gso = galsim.Sersic(kwargs)
        elif profile == 'Exponential':
            gso = galsim.Exponential(kwargs)
        else:
            gso = galsim.DeVeaucouleurs(kwargs)
        
        #Draws the galsim object on a grid    
        source = gso.drawImage(nx=shape[0],
            ny=shape[1],
            use_true_center = True,
            method='real_space',
            scale=self.pix,
            dtype=np.float64).array
        self.image(source)
        return self
    
    
    
    
    
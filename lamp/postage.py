# A few common packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
%matplotlib inline

# We will use astropy's WCS and ZScaleInterval for plotting
from astropy.wcs import WCS
from astropy.visualization import ZScaleInterval
# Also to convert sky coordinates


# We will use several stack functions
import lsst.geom
import lsst.afw.display as afwDisplay
import lsst.afw.display.rgb as rgb

# And also DESC packages to get the data path
import GCRCatalogs
from GCRCatalogs import GCRQuery
import desc_dc2_dm_data




def catalog_setup(dc2_data_version):
    """ This function fetches catalogs and sets up a butler.
    
    Parameters
    ----------
    dc2_data_version: str
        data version of the catalog. This is used to instantiate the butler.
    """
    # Fetch GCR catalogs
    GCRCatalogs.get_available_catalogs(names_only=True, name_contains=dc2_data_version)
    cat = GCRCatalogs.load_catalog("dc2_object_run"+dc2_data_version)
    
    # Sets up butler
    butler = desc_dc2_dm_data.get_butler(dc2_data_version)
    
    
    return cat, butler

def catalog_query(query, columns = None, tracts = None):
    """ Submits a query and a selection to the catalog. Extract relevant information from catalogs.
    
    Parameters
    ----------
    query: str
        a set of selection criteria to select galaxy objects
    tracts: list
        list of tract numbers. Used to restrict the search to a small number of tracts.
    """
    # The minimum set of infomation needed about objects in the catalog
    columns_to_get = ["objectId", "ra", "dec", "tract", "patch"]
    assert cat.has_quantities(columns_to_get)
    
    # Submit the query and get catalog of objects
    if tract is not None:
        filters = f"(tract == {tracts[0]})"
            for t in tracts[1:]:
                filters +=  f" | (tract == {t})"
    objects = cat.get_quantities(columns_to_get, filters=query, native_filters=filters)
    
    # make it a pandas data frame for the ease of manipulation
    objects = pd.DataFrame(objects)
    return objects

def make_postage_stamps(objects, cutout_size=100):
    """ Extracts a coadd postage stamp of an object from the catalog
    
    Parameters
    ----------
    objects: list of GCR catalog entries
        object to cut a postamp out.
    cutout_size: int
        size of the postage stamp to extract in pixels
    
    """
    skymap = butler.get('deepCoadd_skyMap')
    
    cutout_extent = lsst.geom.ExtentI(cutout_size, cutout_size)
    
    radec = lsst.geom.SpherePoint(obj["ra"], obj["dec"], lsst.geom.degrees)
    center = skymap.findTract(radec).getWcs().skyToPixel(radec)
    bbox = lsst.geom.BoxI(lsst.geom.Point2I((center.x - cutout_size*0.5, center.y - cutout_size*0.5)), cutout_extent)

    cutouts = [butler.get("deepCoadd_sub", 
                          bbox=bbox, 
                          tract=object_this["tract"], 
                          patch=object_this["patch"], 
                          filter=band
                         ) for band in "irg"]
    wcs_fits_meta = cutouts[0].getWcs().getFitsMetadata()
    
    return cutouts, wcs_fits_meta

def plot_cutouts(objects, cutout_size=100):
    """ Displays RGB image of cutouts on a mosaic
    """
    cutouts, wcs_fits_meta = make_postage_stamps(objects, cutout_size)
    
    image_rgb = rgb.makeRGB(*cutouts)
    del cutouts  # let gc save some memory for us

    ax = plt.subplot(gs_this, projection=WCS(wcs_fits_meta), label=str(objects["objectId"]))
    ax.imshow(image_rgb, origin='lower')
    del image_rgb  # let gc save some memory for us
    
    for c in ax.coords:
        c.set_ticklabel(exclude_overlapping=True, size=10)
        c.set_axislabel('', size=0)
        
    pass
    
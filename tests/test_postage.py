import numpy.testing as npt
import numpy as np
import pytest

from desclamp import postage


class TestPostage(object):
    
    def test_candidates(self):
        self.candidates = postage.Candidates("2.2i_dr6")
        assert len(self.candidates.cat) == 147088478
        
        bright_galaxy_query = ("clean",
            "extendedness == 1",
            "mag_g_cModel- mag_i_cModel < 5",
            "mag_g_cModel- mag_i_cModel > 1.8",
            "mag_g_cModel- mag_r_cModel < 3",
            "mag_g_cModel- mag_r_cModel > 0.6",
            "mag_r_cModel < 22.5",
            "mag_r_cModel > 18",
            "mag_g_cModel > 20",
            "mag_i_cModel > 18.2",
            "snr_g_cModel > 10",
            "snr_r_cModel > 10",
            "snr_i_cModel > 10",
            )

        self.objects = self.candidates.catalog_query(bright_galaxy_query, tracts=[4639])
        assert len(objects) == 9617
        
        assert all([np.assert_almost_equal(self.objects.loc[0]["ra"]==56.99553034462916), 
                    npt.assert_almost_equal(self.objects.loc[0]["dec"]==-31.207443496107427)
                   ])
        
        
    def test_cutouts(self):
        
        self.cutout = make_postage_stamps(self.objects.loc[0], cutout_size=100, bands = 'irg', inject=None)
        assert all([np.assert_almost_equal(self.cutout.catalog["ra"]==56.99553034462916), 
                    npt.assert_almost_equal(self.cutout.catalog["dec"]==-31.207443496107427)
                   ])
        
        lensed = np.zeros((10,10))
        lensed[4,4]=1
        gsobj = galsim.InterpolatedImage(galsim.Image(lensed), scale = 0.05)
        
        
    def tetst_display(self):
        
        self.candidates.display_cutouts(self.cutout, cutout_size=100, data_range = 2, q = 8)
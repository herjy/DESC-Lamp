import numpy.testing as npt
import numpy as np
import pytest
import galsim
from desclamp import postage


class TestPostage(object):
    
    def setup(self):
        self.candidates = postage.Candidates("2.2i_dr6")
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
        
        lensed = np.zeros((10,10))
        lensed[4,4]=1
        gsobj = galsim.InterpolatedImage(galsim.Image(lensed), scale = 0.05)
        self.cutouts = self.candidates.make_postage_stamps(self.objects.loc[:1], cutout_size=100, bands = 'irg', inject=gsobj)
        
    def test_candidates(self):
        assert len(self.candidates.cat) == 147088478
        assert len(self.objects) == 9617
        
        npt.assert_almost_equal(self.objects.loc[0]["ra"], 56.99553034462916)
        npt.assert_almost_equal(self.objects.loc[0]["dec"], -31.207443496107427)
                  
        
        
    def test_cutouts(self):
        
        npt.assert_almost_equal(self.cutouts[0].catalog["ra"], 56.99553034462916)
        npt.assert_almost_equal(self.cutouts[0].catalog["dec"], -31.207443496107427)
                  
        
        
        
        
    def tetst_display(self):
        
        self.candidates.display_cutouts(self.cutouts, cutout_size=100, data_range = 2, q = 8)
        
if __name__ == '__main__':
    pytest.main()
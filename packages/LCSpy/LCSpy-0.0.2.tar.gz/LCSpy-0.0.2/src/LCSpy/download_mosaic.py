from astropy.io import fits
import numpy as np
import astropy.units as u
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from .LoFAR_cat_search import LoFAR_Cat_Search
import math

def truncate(number, digits):
    nbDecimals = len(str(number).split('.')[1])
    if nbDecimals <= digits:
        return number
    stepper = 10 ** digits
    return math.trunc(stepper * number)/stepper

def format_num(num):
    return str(math.trunc(num)).rjust(2,'0')

class download_mosaic:

    def __init__(self,save_dir,mosaic_id=None):
        self.save_dir = save_dir
        self.mosaic_id = mosaic_id
        self.load_pointing()
        
    def load_pointing(self):
        url_base = 'https://lofar-surveys.org/public/DR2/mosaics/'+str(self.mosaic_id)+'/mosaic-blanked.fits'
        pointingfile = fits.open(url_base)
        pointingfile.writeto(self.save_dir+str(self.mosaic_id)+'full-mosiac.fits')
        pointingfile.close()
        
 

    
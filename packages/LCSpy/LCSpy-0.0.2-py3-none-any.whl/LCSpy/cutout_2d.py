import requests
import math
import numpy as np
import json
from astropy.io import fits 

def truncate(number, digits):
    # Improve accuracy with floating point operations, to avoid truncate(16.4, 2) = 16.39 or truncate(-1.13, 2) = -1.12
    nbDecimals = len(str(number).split('.')[1]) 
    if nbDecimals <= digits:
        return number
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def format_num(num):
    return str(math.trunc(num)).rjust(2,'0')

class cutout_2d:

    def __init__(self,RA,DEC,size):
        self.RA = RA
        self.DEC = DEC
        self.size = size
        self._get_json()
        self.__open_fits()

    def _get_json(self):

        responce = requests.get(self._get_url()).text
        json_responce = json.loads(responce)
        self.image_link = json_responce['data'][3][0]

    def __open_fits(self):
        self.hdul = fits.open(self.image_link)
        #return self.hdul

    def _get_url(self):
        url_start = 'https://vo.astron.nl/hetdex/lotss-dr1-img/cutout/form?__nevow_form__=genForm&hPOS='
        ra = str(self.RA)
        dec = str(self.DEC)
        size=str(self.size)
        url_close = '&hINTERSECT=OVERLAPS&hFORMAT=image%2Ffits&_DBOPTIONS_ORDER=&_DBOPTIONS_DIR=ASC&MAXREC=100&_FORMAT=JSON&submit=Go'
        return url_start+ra+'%2C%20'+dec+'&hSIZE='+size+url_close

        
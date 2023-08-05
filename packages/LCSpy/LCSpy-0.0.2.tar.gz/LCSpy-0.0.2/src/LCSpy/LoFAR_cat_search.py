import requests
import json

class LoFAR_Cat_Search:

    def __init__(self,ra,dec,sr):
        self.__create_url(ra,dec,sr) #assumes they are dics of there h,m,s values.
        self.__get_json()

    def __get_json(self):
        responce = requests.get(self.url).text
        # with bad request, no json is sent!
        try:
            json_data = json.loads(responce)
        except ValueError as e:
                raise Exception('Bad Request, loaction is outside of survey field.') from None
        self.total_data = json_data['data']
        if len(json_data) == 1:
            self.data = self.total_data
        else:
            self.data= self.total_data[0]
        self.Name = self.data[0]
        self.Ra = self.data[1]
        self.Dec = self.data[3]
        self.Mosaic_id = self.data[23] 


    def __create_url(self,ra,dec,sr):
        url_start = 'https://vo.astron.nl/lotss_dr2/q/src_cone/form?__nevow_form__=genForm&hscs_pos='
        rh = str(ra['h'])+'%20'
        rm = str(ra['m'])+'%20'
        rs = str(ra['s'])+'%2C%20'
        dh = str(dec['h'])+'%20'
        dm = str(dec['m'])+'%20'
        ds = str(dec['s'])+'&hscs_sr='
        sr = str(sr)
        url_close = '&_DBOPTIONS_ORDER=&_DBOPTIONS_DIR=ASC&MAXREC=100&_FORMAT=JSON&submit=Go'
        self.url = url_start+rh+rm+rs+dh+dm+ds+sr+url_close

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import json
import time
import csv


class ZillowScraper():
    results = []
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
        'cache-control': 'max-age=0',
        'cookie': 'zjs_user_id=null; _ga=GA1.2.39401405.1636417326; zguid=23|%240e774079-6685-4d46-bf77-3db1d95eace5; _pxvid=122c409f-40f3-11ec-9ed3-6c746f745951; __pdst=40546ac774be4e47a0a569d8a2ba9d9f; _pin_unauth=dWlkPVpURTRNRFpsWmpjdFlXWTBOeTAwWVdZM0xXSmtNbVF0TWpnd05qQmpPVFpoWWpJeg; zjs_anonymous_id=%220e774079-6685-4d46-bf77-3db1d95eace5%22; G_ENABLED_IDPS=google; _cs_c=0; _gcl_au=1.1.1264840185.1644263828; zg_anonymous_id=%22b7cc3adc-88b5-4e41-a819-6fe3a7cc3708%22; g_state={"i_p":1649026128966,"i_l":4}; zgsession=1|47923e3b-033d-4b34-bdbc-95395d04645a; _gid=GA1.2.1259674575.1648081154; KruxPixel=true; DoubleClickSession=true; _cs_id=a2e78b9f-04f1-a123-c788-83f3e5ea0651.1644128748.3.1648081155.1648081155.1.1678292748155; _cs_s=1.5.0.1648082955839; JSESSIONID=AA1A95F1EF0682871714067BE55670E2; utag_main=v_id:017da1801e040023759c319922d605072005906a00fb8$_sn:15$_se:1$_ss:1$_st:1648082954938$dc_visit:15$ses_id:1648081154938%3Bexp-session$_pn:1%3Bexp-session$dcsyncran:1%3Bexp-session$tdsyncran:1%3Bexp-session$dc_event:1%3Bexp-session$dc_region:us-west-2%3Bexp-session$ttd_uuid:32e4f3c3-8227-48ad-bf7e-6d7477395aed%3Bexp-session; KruxAddition=true; _pxff_bsco=1; _clck=sboe6c|1|f01|0; _px3=fe390c30a7ffba16aeda97791b8234447eb6c78a86e242ffffdb43332c15be19:x0G4QRGPXMX1zuO8F9Ifwm84b7PTSkT3FrL+ewGoak7p6E8+mvQChIhu6FXRGQM81dFJVSyt2dywvHiV4WRYEA==:1000:pIul4kwA9YYBS0itOt3bEEOQPygBkAvVIXja8I5G9SIIxRc5YtNw70I0afvAX7dt4Ad6mql8EKsZ/e336DwK6UTsPJVuS607V8RQ2rkAZc51sjfwISBDAh4y/m7OmO/QP0g2BNs60TFy7xyz8DY0Jxk0mT2k57o5ThQeeon7qh3TsUnBErAN4q9m6kJeTPYOo/eT2AFvIT8g3pPkMm9HIA==; _uetsid=a03780f0ab0811ecb8b66936543605e8; _uetvid=c72ea190cf9911eba7a43bfaca316fca; AWSALB=l78tpE9IjeL8h2EyCd08RzdIhsWlrBPQAfTMjtZMj5zsX8m6Pv77VEA8X5b7dtLobeFah0tPjejwcxj+r4Fgqo102V/PTojzBbc25hTzt0ayb6mV1uJJHlyatXcT; AWSALBCORS=l78tpE9IjeL8h2EyCd08RzdIhsWlrBPQAfTMjtZMj5zsX8m6Pv77VEA8X5b7dtLobeFah0tPjejwcxj+r4Fgqo102V/PTojzBbc25hTzt0ayb6mV1uJJHlyatXcT; search=6|1650673459075%7Crect%3D34.15669533155305%252C-118.10171205322266%252C33.885228242538226%252C-118.72175294677734%26rid%3D12447%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26sort%3Ddays%26z%3D1%26type%3Dcondo%252Capartment%26fs%3D0%26fr%3D1%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%26excludeNullAvailabilityDates%3D0%09%0912447%09%09%09%09%09%09; _clsk=1t62agk|1648081459189|7|0|d.clarity.ms/collect',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    }
    

    def fetch(self, url, params):
        response = requests.get(url, headers=self.headers, params=params)
        #print(response.status_code)
        return response


    def parse(self, response):
        content = BeautifulSoup(response)
        deck = content.find('ul', {'class': 'photo-cards photo-cards_wow photo-cards_short'})
        for card in deck.contents:
            script = card.find('script', {'type': 'application/ld+json'})
            #script1 = card.find('address',{'class':'list-card-addr'})
            #script2 = card.find('div',{'class':'list-card-price'})

            if script:
                script_json = json.loads(script.contents[0])

                self.results.append({
                    'floorSize': card.find('ul',{'class': 'list-card-details'}).text,
                    #'details':card.find('ul',{'class':'list-card-details'}).text,
                    'price': card.find('div', {'class': 'list-card-price'}).text,
                    'address':card.find('address',{'class':'list-card-addr'}).text,
                    'website':card.find('a')['href']
                    
                })                

    def to_csv(self):
        with open('zillow.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)    

                
                
                
                
                
#https://www.zillow.com/b/660-N-Oxford-Los-Angeles-CA/34.083244,-118.30799_ll/
                
                
                
    def run(self):
        url = 'https://www.zillow.com/los-angeles-ca/rentals/'

        for page in range(1, 20):
            params = {

                'searchQueryState': '{"pagination":{"currentPage": %s},"usersSearchTerm":"Los Angeles, CA","mapBounds":{"west":-118.72175294677734,"east":-118.10171205322266,"south":33.885228242538226,"north":34.15669533155305},"mapZoom":11,"regionSelection":[{"regionId":12447,"regionType":6}],"isMapVisible":true,"filterState":{"fore":{"value":false},"mf":{"value":false},"ah":{"value":true},"sort":{"value":"days"},"auc":{"value":false},"nc":{"value":false},"fr":{"value":true},"sf":{"value":false},"land":{"value":false},"tow":{"value":false},"manu":{"value":false},"fsbo":{"value":false},"cmsn":{"value":false},"fsba":{"value":false}},"isListVisible":true}' %page

            }
            res = self.fetch(url, params)
            self.parse(res.text)
            time.sleep(2)
        self.to_csv()


if __name__ == '__main__':
    scraper = ZillowScraper()
    scraper.run()


# In[ ]:





# In[ ]:





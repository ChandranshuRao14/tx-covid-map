import requests, json, os
from bs4 import BeautifulSoup, NavigableString
from flask import Flask, render_template

API_KEY = os.environ.get('MAPS_API_KEY')

class TestingSite:
    def __init__(self, metro, name, addr, website):
        self.metro = metro
        self.name = name
        self.addr = addr
        self.website = website
        self.getLocation()

    def getLocation(self):
        query = self.addr.replace(' ', '+')
        geoURL = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + query + '&key=' + API_KEY
        req = requests.get(geoURL).json()
        print(req)
        if req['status'] == 'OK':
            results = req['results'][0]
            self.addr = results['formatted_address']
            print(self.addr)
            self.lat = results['geometry']['location']['lat']
            self.long = results['geometry']['location']['lng']
            print(self.lat)
        else:
            self.lat = 30
            self.long = -94

    def to_dict(self):
        return {"metro": self.metro, "name": self.name, "address": self.addr, "website": self.website, "lat": self.lat, "long": self.long}

def scrape():
    # request Texas DSHS url
    URL = 'https://www.dshs.state.tx.us/coronavirus/testing.aspx'
    page = requests.get(URL, verify=False)

    # Parse HTML
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='ctl00_ContentPlaceHolder1_uxContent')
    divider = results.find('ul')
    sites = divider.find_all_next('h3')

    testing_sites = []

    # Get all sites and create object
    for site in sites:
        metro = site.find_previous('h2')
        info = site.find_next('p')
        website = info.find_next('a')
        addresses = []
        # Get all addresses for the testing site
        for i in info.contents:
            if isinstance(i, NavigableString) and i != '\n':
                cleaned = i.strip(' \n').strip('|')
                if '|' in cleaned:
                    addresses.extend(cleaned.split('|'))
                else: addresses.append(cleaned)
        # Create new Site object
        for add in addresses: 
            testing_sites.append(TestingSite(metro.string, site.string, add.strip(), website['href']))

    return testing_sites

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    sites = scrape()
    results = [obj.to_dict() for obj in sites]
    data = json.dumps({"results": results})
    return render_template('index.html', data=data, API_KEY=API_KEY)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
import requests, json, os, certifi
from google.cloud import secretmanager, storage
from bs4 import BeautifulSoup, NavigableString, Tag

# Project values
project_id = os.environ['PROJECT_ID']
secret_name = 'maps-secret'
bucket_name = os.environ['BUCKET_NAME']

# Access Google Maps API Key from Secrets Manager
secret_client = secretmanager.SecretManagerServiceClient()
name = secret_client.secret_version_path(project_id, secret_name, 'latest')
response = secret_client.access_secret_version(name)
API_KEY = response.payload.data.decode('UTF-8')

class TestingSite:
    def __init__(self, metro, name, address, websites):
        self.metro = metro
        self.name = name
        self.address = address
        self.websites = websites
        self.getLocation()

    def getLocation(self):
        # Get full address from Geocode API
        query = self.address.replace(' ', '+').replace('#', '')
        geoURL = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + query + '&key=' + API_KEY
        req = requests.get(geoURL).json()

        # Check status of the request
        if req['status'] == 'OK':
            results = req['results'][0]
            self.address = results['formatted_address']
            self.lat = results['geometry']['location']['lat']
            self.long = results['geometry']['location']['lng']

    def to_dict(self):
        return {"metro": self.metro, "name": self.name, "address": self.address, "websites": self.websites, "lat": self.lat, "long": self.long}

# Scrape Texas DSHS website for drive-thru data
def scrape():
    URL = 'https://www.dshs.state.tx.us/coronavirus/testing.aspx'
    page = requests.get(URL, verify=False)

    body = BeautifulSoup(page.content, 'html.parser')
    content = body.find(id='ctl00_ContentPlaceHolder1_uxContent')
    sites = content.find_all_next('h3')
    last_element = content.find_all_next('hr')[-1]
    testing_sites = []
    
    for site in sites:
        metro = site.find_previous('h2')
        addresses = []
        websites = []
        for e in site.next_elements:
            if e in sites or e == last_element: break
            if isinstance(e, NavigableString):
                if e != '\n' and e != ' ' and any(char.isdigit() for char in e) and 'COVID' not in e:
                    cleaned = e.strip(' \n-')
                    addresses.append(cleaned)
            elif isinstance(e, Tag) and e.name == 'a':
                if e['href'] != "#top": websites.append(e['href'])

        # Create new TestingSite object and append to list
        if len(addresses) == 0: testing_sites.append(TestingSite(metro.string, site.string, f'{site.string} {metro.string}', websites))
        else: testing_sites.extend([TestingSite(metro.string, site.string, address, websites) for address in addresses])

    return testing_sites

def main(request):
    # Get results
    sites = scrape()
    results = [obj.to_dict() for obj in sites]
    data = json.dumps({"results": results})

    # Upload to bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob('results.json')
    blob.upload_from_string(data)

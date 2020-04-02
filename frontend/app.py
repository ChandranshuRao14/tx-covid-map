import requests, json, os
from google.cloud import secretmanager, storage
from flask import Flask, render_template

# Project values
project_id = os.environ['PROJECT_ID']
secret_name = 'maps-secret'
bucket_name = os.environ['GCP_BUCKET']

app = Flask(__name__)

# Access Google Maps API Key from Secrets Manager
def getApiKey():
    secret_client = secretmanager.SecretManagerServiceClient()
    name = secret_client.secret_version_path(project_id, secret_name, 'latest')
    response = secret_client.access_secret_version(name)
    key = response.payload.data.decode('UTF-8')

    return key

# Grab latest results from GCS bucket
def getLatestResults():
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob('results.json')
    data = blob.download_as_string()

    return data

# Serve homepage
@app.route('/', methods=['GET'])
def index():
    api_key = getApiKey()
    data = getLatestResults()

    return render_template('index.html', data=data, API_KEY=api_key)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
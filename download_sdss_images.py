import os
import pandas as pd
import requests

CSV_FILE = 'sdss_data.csv'
OUTPUT_DIR = 'sdss_images'
IMAGE_SIZE = 512
SCALE = 0.396 # SDSS Default Arcsec/pixel
BAND = 'g'

# os.makedirs(OUTPUT_DIR, exist_ok = True)

# Query SDSS Data Release 18's SQL Server

sdss_url = 'https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/SqlSearch'
sql_query = \
"""
SELECT TOP 1000 ra, dec
FROM PhotoObj
WHERE type = 3 AND clean = 1
"""
params = \
{
    'cmd': sql_query,
    'format': 'csv'
}

print('Querying galaxy coordinates into csv file...')

try:
    response = requests.get(sdss_url, params = params)
    response.raise_for_status()
    
    with open(CSV_FILE, 'w', encoding = 'utf-8') as f:
        f.write(response.text)
    
except requests.exceptions.RequestException as e:
    print(f'An error occured: {str(e)}')
    exit()


df = pd.read_csv(CSV_FILE)
print(f'Successfully loaded {len(df)} galaxy coordinates.')
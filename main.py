import os
import sys
import requests
import json
from bs4 import BeautifulSoup
import logging
import time

start_time = time.time()
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

with open('config.json') as f:
    config = json.load(f)

api_key = os.getenv('API_KEY')
base_url       = config['base_url']
workspace_name = config['workspace_name']
links          = config['links']

logging.info(f'base_url: {base_url}')
logging.info(f'workspace_name: {workspace_name}')
logging.info(f'links: {links}')

if api_key:
    logging.info(f'api_key={"*" * len(api_key)}')
else:
    logging.error('No API key found')
    sys.exit(1)

headers = {
    'accept': 'application/json',
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

def get_workspace_slug(workspace_name):
    url = f'{base_url}/api/v1/workspaces'
    response = requests.get(url, headers=headers)
    data = response.json()

    for workspace in data['workspaces']:
        if workspace['name'] == workspace_name:
            logging.info(f"slug {workspace['slug']} for name {workspace['name']} found")
            return workspace['slug']

    logging.error(f'Workspace {workspace_name} not found')
    sys.exit(1)

slug = get_workspace_slug(workspace_name)

def list_subpages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    subpages = []

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/'):
            subpages.append(url + href)

    return subpages

def post_document_upload_link(url):
    api_url = f'{base_url}/api/v1/document/upload-link'
    data = {
        'link': url,
    }
    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        data = response.json()
        return data['documents'][0]['location']
    else:
        logging.error(f"{url} can't be fetched")
        sys.exit(1)

def update_embeddings(filelocation):
    url = f'{base_url}/api/v1/workspace/{slug}/update-embeddings'
    data = {
        "adds": [f"{filelocation}"],
        "deletes": [""]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    return response

for link in config['links']:
    pages = list_subpages(link)
    for page in pages:
        filelocation = post_document_upload_link(page)
        update_embeddings(filelocation)
    logging.info(f'Uploaded {len(pages)} documents from {link}')

end_time = time.time()
execution_time = end_time - start_time
logging.info(f'Execution time: {round(execution_time, 2)} seconds')
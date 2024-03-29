import os
import glob
from google_images_search import GoogleImagesSearch
from dotenv import load_dotenv
import json
import requests
import io

# Environment variables 
load_dotenv()

# setting dev key and cx
gis = GoogleImagesSearch(os.getenv('GCS_DEV_KEY'), os.getenv('GCS_ID'))

# Create the images directory if it doesn't exist
if not os.path.exists('./images/'):
    os.makedirs('./images/')

# function to getcall and download
def get_images(query, n):
    _search_params = {
        'q': query,
        'num': n,
        'fileType': 'jpg|gif|png',
    }
    try:
        gis.search(search_params=_search_params, path_to_dir='./images/')
        filenames = [f for f in os.listdir('./images/') if os.path.isfile(os.path.join('./images/', f))]
        if len(filenames) > 0:
            return filenames
        else:
            print("No images found.")
            return []
    except Exception as e:
        print(e)

def search_pexels_images(query):
    API_KEY = os.getenv('PEXELS_KEY')

    # extract keyword
    query = query.split()[0].lower()
    print(query)
    PEXELS_API_URL = f'https://api.pexels.com/v1/search?query={query}&per_page=1'

    headers = {
        'Authorization': API_KEY
    }

    response = requests.get(PEXELS_API_URL, headers=headers)

    data = json.loads(response.text)

    if 'photos' in data:
        if len(data['photos']) > 0:
            return data['photos'][0]['src']['medium']

    return None


# function to empty the images folder
def empty_images():
    folder_path = "./images/"
    file_list = glob.glob(os.path.join(folder_path, "*"))
    for file_path in file_list:
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
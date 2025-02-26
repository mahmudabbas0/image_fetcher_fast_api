import requests
import os
import shutil
import random
from dotenv import load_dotenv
from googletrans import Translator

load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
FLICKR_API_KEY = os.getenv("FLICKR_API_KEY")
FLICKR_API_SECRET = os.getenv("FLICKR_API_SECRET")

translator = Translator()

STATIC_DIR = "static"
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

def clean_static_folder():
    try:
        for filename in os.listdir(STATIC_DIR):
            file_path = os.path.join(STATIC_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    except Exception as e:
        raise Exception(f"static Klasör temizlenemedi : {str(e)}")

def translate_to_english(query):
    try:
        detected = translator.detect(query)
        if detected.lang != 'en':
            translated = translator.translate(query, dest='en')
            return translated.text
        return query
    except Exception:
        return query

def fetch_images_from_unsplash(query, num_images, page=None):
    if not UNSPLASH_ACCESS_KEY:
        return []
    try:
        page = random.randint(1, 10) if page is None else page
        url = f"https://api.unsplash.com/search/photos?query={query}&per_page={num_images}&page={page}&client_id={UNSPLASH_ACCESS_KEY}"
        response = requests.get(url)
        if response.status_code != 200:
            return []
        data = response.json()
        return [photo["urls"]["regular"] for photo in data["results"]]
    except Exception:
        return []

def fetch_images_from_pexels(query, num_images, page=None):
    if not PEXELS_API_KEY:
        return []
    try:
        page = random.randint(1, 10) if page is None else page
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/v1/search?query={query}&per_page={num_images}&page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return []
        data = response.json()
        return [photo["src"]["medium"] for photo in data["photos"]]
    except Exception:
        return []

def fetch_images_from_flickr(query, num_images, page=None):
    if not FLICKR_API_KEY or not FLICKR_API_SECRET:
        return []
    try:
        page = random.randint(1, 10) if page is None else page
        url = f"https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key={FLICKR_API_KEY}&text={query}&per_page={num_images}&page={page}&format=json&nojsoncallback=1"
        response = requests.get(url)
        if response.status_code != 200:
            return []
        data = response.json()
        if "photos" not in data or "photo" not in data["photos"]:
            return []
        photos = data["photos"]["photo"]
        return [f"https://live.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}_m.jpg" for photo in photos]
    except Exception:
        return []

def download_image(url, query, index):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            response.raw.decode_content = True
            file_path = os.path.join(STATIC_DIR, f"{query}_{index}.jpg")
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            return f"/static/{query}_{index}.jpg"
        return None
    except Exception:
        return None

def fetch_images(query, num_images=3):
    clean_static_folder()

    translated_query = translate_to_english(query)

    fetch_count = num_images * 2

    unsplash_images = fetch_images_from_unsplash(translated_query, fetch_count) if UNSPLASH_ACCESS_KEY else []
    pexels_images = fetch_images_from_pexels(translated_query, fetch_count) if PEXELS_API_KEY else []
    flickr_images = fetch_images_from_flickr(translated_query, fetch_count) if FLICKR_API_KEY and FLICKR_API_SECRET else []

    all_image_urls = list(set(unsplash_images + pexels_images + flickr_images))
    
    random.shuffle(all_image_urls)
    selected_urls = all_image_urls[:num_images]

    saved_image_paths = []
    for i, url in enumerate(selected_urls):
        saved_path = download_image(url, translated_query, i)
        if saved_path:
            saved_image_paths.append(saved_path)
    
    if not saved_image_paths and not any([UNSPLASH_ACCESS_KEY, PEXELS_API_KEY, FLICKR_API_KEY and FLICKR_API_SECRET]):
        raise ValueError("Lütfen .env dosyasına en az bir API anahtarı girin")
    
    return saved_image_paths
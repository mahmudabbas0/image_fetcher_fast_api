# Image Fetcher API

A FastAPI-based application that fetches random images from multiple online sources (Unsplash, Pexels, Flickr) based on a user-provided query. The project supports multi-language input by translating non-English queries to English, stores the fetched images locally in a `static` folder, and ensures that old images are cleared before fetching new ones with each request.

## Features
- **Multi-Source Image Fetching**: Retrieves random images from Unsplash, Pexels, and Flickr.
- **Randomization**: Ensures fresh, random images with each request using random page selection and shuffling.
- **Language Support**: Automatically translates non-English queries to English using Google Translate.
- **Local Storage**: Downloads and stores images in a `static` folder, serving them via the API.
- **Folder Cleanup**: Deletes old images from the `static` folder before fetching new ones.
- **Flexible API Keys**: Works with at least one valid API key from any supported source.

## Prerequisites
- **Python**: Version 3.8 or higher.
- **API Keys**: At least one API key from Unsplash, Pexels, or Flickr (see [Setup](#setup) for details).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/mahmudabbas0/image_fetcher_fast_api.git
   cd image-fetcher-api

## Requirements

```bash
pip install fastapi uvicorn requests python-dotenv googletrans==3.1.0a0

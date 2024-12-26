import os
import requests
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_image(url, filename):
    """Download an image from URL and save it to assets/photos directory."""
    # Create assets/photos directory if it doesn't exist
    photos_dir = Path('assets/photos')
    photos_dir.mkdir(parents=True, exist_ok=True)

    # Full path for the image
    image_path = photos_dir / filename
    logging.info(f"Attempting to download image from {url} to {image_path}")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.timesofisrael.com/'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Verify content type is an image
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            raise ValueError(f"Invalid content type: {content_type}")

        # Save the image
        with open(image_path, 'wb') as f:
            f.write(response.content)

        logging.info(f"Successfully downloaded {filename}")
        return True

    except Exception as e:
        logging.error(f"Error downloading {filename}: {str(e)}")
        return False

if __name__ == "__main__":
    # List of images to download
    images = [
        {
            'url': 'https://static.timesofisrael.com/www/uploads/2023/10/WhatsApp-Image-2023-10-08-at-13.44.49.jpeg',
            'filename': 'doron-asher.jpg'
        }
    ]

    # Download all images
    for image in images:
        if not download_image(image['url'], image['filename']):
            logging.error(f"Failed to download {image['filename']}")
            exit(1)

    logging.info("All images downloaded successfully")
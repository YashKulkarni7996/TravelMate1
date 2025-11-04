import requests
import os
from tqdm import tqdm

def download_file(url):
    # Get the file name from the URL
    filename = url.split('/')[-1]
    
    # Send a GET request with stream=True to download large files efficiently
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    # Get the file size from headers
    file_size = int(response.headers.get('content-length', 0))
    
    # Create a progress bar
    progress = tqdm(total=file_size, unit='iB', unit_scale=True)
    
    # Open file and write chunks
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                size = file.write(chunk)
                progress.update(size)
    
    progress.close()
    
    # Print file info
    if os.path.exists(filename):
        size_mb = os.path.getsize(filename) / (1024 * 1024)
        print(f"\nDownloaded: {filename}")
        print(f"Size: {size_mb:.2f} MB")

def main():
    url = "https://dumps.wikimedia.org/enwikivoyage/latest/enwikivoyage-latest-pages-articles-multistream.xml.bz2"
    print("Starting download...")
    try:
        download_file(url)
        print("Download completed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
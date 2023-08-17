from bing_image_downloader import downloader

def get_images(query):
    try:
        downloader.download(query+" face", limit=5,  output_dir='download', 
        adult_filter_off=True, force_replace=False, timeout=60)
    except FileNotFoundError:
            pass
    print()

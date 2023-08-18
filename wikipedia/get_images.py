from bing_image_downloader import downloader
from PIL import Image
import os


def get_images(query):
    try:
        downloader.download(query+" face", limit=5,  output_dir='download', 
        adult_filter_off=True, force_replace=False, timeout=60)
    except FileNotFoundError:
            pass
    print()


# def convert_to_jpg(name):
#    directory = rf"C:\Users\Peam\iCloudDrive\Notion API\download\{name} face"
#    for filename in os.listdir(directory):
#        f = os.path.join(directory, filename)
#        im = Image.open(f)       
#        # converting to jpg
#        rgb_im = im.convert("RGB")
        # exporting the image
#        rgb_im.save(filename[:7]+".jpg")
#        print (f)

def convert_to_jpg(name):
    directory = rf"C:\Users\Peam\iCloudDrive\Notion API\download\{name} face"
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        f_split = (os.path.join(directory, filename)).split(".")
        jpg = ".jpg"
        os.rename(f, f_split[0]+jpg)

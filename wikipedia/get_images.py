from google_images_download import google_images_download
 
# creating object
response = google_images_download.googleimagesdownload()
  
def downloadimages(query):
    # keywords is the search query
    # limit is the number of images to be downloaded
    # print urls is to print the image file url
    # size can be specified manually ("large, medium, icon")
    # aspect ratio ("tall, square, wide, panoramic")
    arguments = {"keywords": query,
                 "format": "jpg",
                 "limit":10,
                 "print_urls":True,
                 "size": "large",
                 "aspect_ratio":"wide"}
    try:
        paths = response.download(arguments)
     
    # Handling File NotFound Error   
    except FileNotFoundError:
        arguments = {"keywords": query,
                     "format": "jpg",
                     "limit":4,
                     "print_urls":True,
                     "size": "medium"}
                      
        # Providing arguments for the searched query
        try:
            # Downloading the photos based on the given arguments
            paths = response.download(arguments)
        except:
            pass
    return paths
 
def get_images(list):
    for query in list:
        paths = downloadimages(query)
        print(paths)

artist_names = ["Henri Rousseau", "Leonora Carrington", "Cindy Sherman"]
get_images(artist_names)

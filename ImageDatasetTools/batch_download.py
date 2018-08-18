from google_images_download import google_images_download
limit = 1000
path = "chromedriver"
file = open("keywordlist.txt")
for line in file:
    keyword = line.rstrip()
    response = google_images_download.googleimagesdownload()
    arguments = {"keywords":keyword,"limit":limit, "chromedriver":path}   #creating list of arguments
    paths = response.download(arguments)   #passing the arguments to the function
    #print(paths)   #printing absolute paths of the downloaded images
file.close()

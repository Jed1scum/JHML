#!/usr/bin/env python
# Batch thumbnail generation script using PIL
#http://www.coderholic.com/batch-image-processing-with-python/
import sys
import os
from PIL import Image
#converts images to jpg format and cleans path e.g. removes white space.

def main(argv):
    rootFolderPath = argv[0]
    #make a "clean directory"
    #cleanPath = os.path.join(rootFolderPath, "clean")
    #if not os.path.exists(cleanPath):
    #    os.makedirs(cleanPath)
    for subdir, dirs, files in os.walk(rootFolderPath):
        for name in files:
            imagePath = os.path.join(subdir, name)
            #strip white space
            print(imagePath)
            convertTojpg(imagePath)
        #for name in dirs:
        #    print(os.path.join(rootFolderPath, name))

        #print("main")
        #print(dirs)
        #for file in files:
        #    print (os.path.join(str(subdir), str(file)))

    #pngTojpg(inputfile)

def convertTojpg(inputfile):

    finalPath = ""
    try:
        #open the file
        image = Image.open(inputfile)
        #confirm the image is not corrupted
        image.verify() # verify that it is, in fact an image
    except (IOError, SyntaxError) as e:
        print('Bad file:', inputfile) # print out the names of corrupt files

    try:
        # Attempt to open an image file
        filepath = inputfile

        #remove whitespace in the name
        cleanPath = filepath.replace(" ","")
        os.rename(filepath, cleanPath)

        #open the file
        image = Image.open(cleanPath)
        #delete the
        # Resize the image
        #image = image.resize(thumbnail_size, Image.ANTIALIAS)
        #Split our original filename into name and extension
        (name, extension) = os.path.splitext(cleanPath)

        #save image wth valid jpg extension
        finalPath = name + '.jpg'
        image.save(finalPath)
        # Save the thumbnail as "(original_name)_thumb.png"
    except IOError as e:
    # Report error, and then skip to the next argument
        print ("Problem opening", filepath, ":", e)

    

    

        

if __name__=="__main__":
    main(sys.argv[1:])

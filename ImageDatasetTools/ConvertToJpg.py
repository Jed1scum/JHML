#!/usr/bin/env python
# Batch thumbnail generation script using PIL
#http://www.coderholic.com/batch-image-processing-with-python/
import sys
import os
from PIL import Image
import shutil
 
discardFolderPath = ""
def move(src, dest):
    shutil.move(src, dest)

#converts images to jpg format and cleans path e.g. removes white space.


def main(argv):
	rootFolderPath = argv[0]
	#create a discard folder 
	discardFolderPath = os.path.join(rootFolderPath, "discard")
	if not os.path.exists(discardFolderPath):
		os.makedirs(discardFolderPath)

	
	for subdir, dirs, files in os.walk(rootFolderPath):
		for name in files:
			imagePath = os.path.join(subdir, name)
			#strip white space
			print(imagePath)
			convertTojpg(imagePath, rootFolderPath)
        #for name in dirs:
        #    print(os.path.join(rootFolderPath, name))

        #print("main")
        #print(dirs)
        #for file in files:
        #    print (os.path.join(str(subdir), str(file)))

    #pngTojpg(inputfile)

def convertTojpg(inputfile, rootFolder):

    finalPath = ""
    discardFolderPath = os.path.join(rootFolder, "discard")
    try:
        #open the file
        image = Image.open(inputfile)
        #confirm the image is not corrupted
        image.verify() # verify that it is, in fact an image
    except (IOError, SyntaxError) as e:
        print('!!!!!!!!! Bad file:', inputfile) # print out the names of corrupt files
        #move the file to the discard folder, that was already created
        (name, extension) = os.path.splitext(inputfile)
        deletePath = os.path.join(discardFolderPath, os.path.basename(inputfile))
        #print("#### "+ deletePath)
        move(inputfile, deletePath)

    try:
        # Attempt to open an image file
        filepath = inputfile
        #open the file
        image = Image.open(filepath)
        #remove whitespace in the name
        #cleanPath = filepath.replace(" ","")
        #os.rename(filepath, cleanPath)

        #convert to rgb just in case
        image = image.convert('RGB')
        #delete the
        # Resize the image
        #image = image.resize(thumbnail_size, Image.ANTIALIAS)

        #save
        #image.save(filepath)
        #Split our original filename into name and extension
        (name, extension) = os.path.splitext(filepath)
        #save image wth valid jpg extension
        finalPath = name + '.jpg'
        finalPath = finalPath.replace(" ","")
        os.rename(filepath, finalPath)
        # Save the thumbnail as "(original_name)_thumb.png"

    except IOError as e:
    # Report error, and then skip to the next argument
        print ("Problem opening", filepath, ":", e)


if __name__=="__main__":
    main(sys.argv[1:])

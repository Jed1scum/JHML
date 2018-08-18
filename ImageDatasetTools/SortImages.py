import scripts/JH_label_image
import shutil


#how accurate we need to be
threshold = .99
def move(src, dest):
    shutil.move(src, dest)


#look at each image in a folder and determine if it looks anything like what it is supposed to be.
#exec(open("scripts/JH_label_image.py").read())

def main(argv):
	#apply image classify to a folder and count the number of results
	directory = argv
	files = 0
	correct = 0

	#create a discard folder for images we can't sorts
	discardFolderPath = os.path.join(directory, "discard")
	if not os.path.exists(discardFolderPath):
	    os.makedirs(discardFolderPath)

	for subdir, dirs, folder in os.walk(directory):
	    for file in folder:
	        
	        (name, extension) = os.path.splitext(file)
	        #only process images with .jpg extension
	        if(extension == ".jpg"):
	            files+=1
	            filePath = os.path.join(subdir,file)
	            #print(filePath)
	            #run ml on the image and save the first text reults
	            resultValue= ""
	            try:
	                print("reading "+filePath)
	                resultLabel,resultValue = label_image(filePath)
	                test = str(os.path.basename(subdir))
	                print(str(files)+ "Test "+" : "+test + " == " + resultLabel +"\n")
	            except IOError as e:
	                print("Problem classifying", filePath, ":", e)
	                resultLabel = "discard"
	                
	            #discardFolderPath = os.path.join(directory, str(resultLabel))
	            #(name, extension) = os.path.splitext(filePath)
	            #if the image result is above the threshhold then move it to the label directory
	            if(resultValue >= threshold):
	                destPath = os.path.join(directory, resultLabel)
	            else:
	                resultLabel = "discard"
	                destPath = os.path.join(directory, resultLabel)
	  
	            #print(destPath)
	            try:
	                move(filePath, destPath)
	            except IOError as e:
	            # Report error, and then skip to the next argument
	                print ("Problem moving", filePath, ":", e)

if __name__=="__main__":
    main(sys.argv[1:])
            
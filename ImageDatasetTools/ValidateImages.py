import scripts/JH_label_image
import shutil

#apply image classify to a folder and count the number of results
directory = "tf_files/sort/fork"
files = 0
correct = 0


def main(argv):
	for subdir, dirs, folder in os.walk(directory):
	    for file in folder:
	        
	        (name, extension) = os.path.splitext(file)
	        #only process images with .jpg extension
	        if(extension == ".jpg"):
	            files+=1
	            filePath = os.path.join(subdir,file)
	            #print(filePath)
	            #run ml on the image and save the first text reults
	            print(filePath)
	            resultLabel, resultValue = label_image(filePath)
	            test = str(os.path.basename(subdir))
	            
	            if(test == resultLabel):
	                correct+=1
	                print(str(files)+ " CORRECT: Test "+" : "+test + " == " + resultLabel +"\n")
	                print(resultValue)
	                #print(str(files) + ":" +str(resultText)+"\n")
	            else:
	                print(str(files) + " INCORRECT!! Test "+":" +test + " != " + resultLabel+"\n")
	            
	print(str(correct) + " out of " + str(files) + " : " + str(files/correct))      


if __name__=="__main__":
    main(sys.argv[1:])
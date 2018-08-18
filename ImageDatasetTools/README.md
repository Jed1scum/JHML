#ImageDatasetTools Project

The project has aimed to create an easy to use workflow for image classification

Step1: 
Download images to labeled folders under tf_files/data directory
Use batch_download.py if to scrape google images 
 - add searched label keywords to keywordlist.txt


Step2:
Clean the downloaded images with ConvertToJpg.py <rootPath>
If there are too many files to validate they are good training images. Create a temp training folder with around 100 images per label and create the model off that.


Step3: 
Run the scripts/retrain.py script on the root folder e.g. tf_files/data folder 
or
tf_files/tempData folder

Step 4: 
Move images into the discard folder if they don't belong to the label by running the SortImages.py <rootpath>

Step 5: 
Take a new test set of data and evaluate if they are correctly identified. Run SortImages.py <rootpath>
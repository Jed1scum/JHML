import requests
#help from
#https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts/python-disk
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from PIL import Image
from io import BytesIO
import os
import datefinder

# Replace <Subscription Key> with your valid subscription key.
subscription_key = "2eaebc8c15a84418a9766a3f3b20ca40"
assert subscription_key

# You must use the same region in your REST call as you used to get your
# subscription keys. For example, if you got your subscription keys from
# westus, replace "westcentralus" in the URI below with "westus".
# Free trial subscription keys are generated in the westcentralus region.
# If you use a free trial subscription key, you shouldn't need to change
# this region.

#Helper method to show the pillow image processing that occured
def ShowImageResult():
	plt.axis("off")
	plt.show()

#helper method, given a meta data structure, return just the text in a list
def FindWordsInLine(line):
	lineText = []
	for word_metadata in line:
		lineText.append(word_metadata['text'])
	return lineText

#method to request that an image is analysed for text using MS Azure congnitive OCR services and return a data structure of the text with text box information
def RequestOCRProcessing(url,showResult):
	vision_base_url = "https://australiaeast.api.cognitive.microsoft.com/vision/v2.0/"
	ocr_url = vision_base_url + "ocr"

	# Set image_url to the URL of an image that you want to analyze.
	image_url = url
	#"https://d85ecz8votkqa.cloudfront.net/support/help_center/Print_Payment_Receipt.JPG"
	#"http://media-s3-us-east-1.ceros.com/ozy/images/2017/12/15/cd09ad332e974fd19dba422a130a313b/convo-1-text-13.png"
	#"https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/" + \ "Broadway_and_Times_Square_by_night.jpg/450px-Broadway_and_Times_Square_by_night.jpg"

	
	params  = {'language': 'unk', 'detectOrientation': 'true'}
	#{'mode': 'Categories,Description,Color'}
	data    = {'url': image_url}
	image_data = []
	#if we can simply open the url/path then its a path to a local file. Otherwise treat it as a url
	if os.path.exists(url):
		headers = {'Content-Type': 'application/octet-stream','Ocp-Apim-Subscription-Key': subscription_key }
		image_data = open(url, "rb").read()
		response = requests.post(ocr_url, headers=headers, params=params, data=image_data)
	else:
		headers = {'Ocp-Apim-Subscription-Key': subscription_key }
		response = requests.post(ocr_url, headers=headers, params=params, json=data)

	response.raise_for_status()
	# The 'analysis' object contains various fields that describe the image. The most
	# relevant caption for the image is obtained from the 'description' property.
	analysis = response.json()
	
	#print(analysis)
	# Extract the word bounding boxes and text.
	line_infos = [region["lines"] for region in analysis["regions"]]
	word_infos = []
	for line in line_infos:
		for word_metadata in line:
			for word in word_metadata["words"]:
				word_infos.append(word)
	
	# Display the image and overlay it with the extracted text.
	
	if(showResult):
		plt.figure(figsize=(5, 5))
		#try to open the local file, otherwise its probably a url
		try:
			image = Image.open(BytesIO(requests.get(image_url).content))
		except ValueError:
			image = Image.open(BytesIO(image_data))

		ax = plt.imshow(image, alpha=0.5)
		for word in word_infos:
			bbox = [int(num) for num in word["boundingBox"].split(",")]
			text = word["text"]
			origin = (bbox[0], bbox[1])
			patch  = Rectangle(origin, bbox[2], bbox[3], fill=False, linewidth=2, color='y')
			ax.axes.add_patch(patch)
			plt.text(origin[0], origin[1], text, fontsize=5, weight="bold", va="top")
		ShowImageResult()
	return word_infos#line_infos


#determine if a string is of decimal type i.e. 2.0 rather than just 2
def isDecimalType(word):
	try:
		float(word)
		try:
			int(word)
			return False
		except ValueError:
			return True
	except ValueError:
		return False
	return value

#Search a data structure of text and pull out just the decimal values, likely to be price lists
def SearchDataForDecimal(data):
	wordGroups = data
	prices = []
	for group in wordGroups:
		thisGroup= []
		text = group['text']
		currentBouding = group['boundingBox']
		thisGroup.append(text)
		
		for word in thisGroup:
			#also strip out any dollar signs found
			word = word.strip('$')
			if(isDecimalType(word)):
				prices.append(float(word))
	
	return prices
#Search a data structure of text and pull out anything that looks like it may help describe what the reciept was used for
def SearchForDescription(data):
	wordGroups = data
	description = []
	for group in wordGroups:
	#just look at the first group for the description, its often the first thing listed
		#print(group)
		thisGroup= []
		text = group['text']
		currentBouding = group['boundingBox']
		thisGroup.append(text)
			
		for word in thisGroup:
			description.append(word)
	#print(description)
	return description

#search the datastructure for anything that resembles a date. for what ever reason i can't work out it returns the current date with the detected date. 
#when the return value is passed you can just select the first element. If i do it in the current method it throws an error
def SearchForDate(data):
	wordGroups = data
	dateData = []
	allData = []
	index = 0
	for group in wordGroups:
		index +=1
		thisGroup= []
		text = group['text']
		currentBouding = group['boundingBox']
		thisGroup.append(text)
		for word in thisGroup:
			#if(isDecimalType(word)):
			#use datefinder to see if the word is a date, if it is we will save it out
			matches = list(datefinder.find_dates(word))
			allData.append(word)
			if len(matches) > 0:
				firstMatches = matches[0].strftime("%x")
				dateData.append(firstMatches)
	#if we didn't find any dates, i.e. the image was blurry or nothing to find, then just put an unknown
	if(len(dateData)==0):
		dateData.append("Unknown")
	return dateData

def SearchForCCType(data):
	wordGroups = data
	ccData = []
	allData = []
	index = 0
	ccList = ['visa','mastercard', 'master card', 'amex', 'american express', 'nabvisa']
	for group in wordGroups:
		index +=1
		thisGroup= []
		text = group['text']
		currentBouding = group['boundingBox']
		thisGroup.append(text)
		for word in thisGroup:
			#if(isDecimalType(word)):
			#use WordInDict to see if the word is a matching with a cc type
			if(WordInDict(word,ccList)):
				ccData.append(word)
	#if we didn't find any dates, i.e. the image was blurry or nothing to find, then just put an unknown
	if(len(ccData)==0):
		ccData.append("Unknown")
	return ccData

def WordInDict(word, dict):
	#convert the word to lowercase to make this even
	if word.lower() in dict:
		return True
	else:
		return False
#given a list of numbers, retur the highest one
def GetHighest(data):
	highest = []
	if(len(data) >0):
		highest = max(data)
	return highest



#####where the magic happens
'''
thisUrl = "https://media-cdn.tripadvisor.com/media/photo-s/0f/12/7d/69/bill-for-2-april-2017.jpg"    
requestData = RequestOCRProcessing(thisUrl)
priceList = SearchDataForDecimal(requestData)

print(priceList)
print(GetHighest(priceList))
'''

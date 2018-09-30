import Reciept
import pandas as pd
import datetime

#take a series of images in a folder
#process each one sing the analyse reciept scripts
#save the relevent data to a csv

import sys, getopt, os

def main(argv):
   inputfolder = argv[0]
   try:
   	opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
   	print ('AnalyseRecipet.py -i <inputfolder> -o <outputfile>')
   	sys.exit(2)
   	for opt, arg in opts:
   		if opt == '-h':
   			print ('AnalyseReciept.py -i <inputfile> -o <outputfile>')
   			sys.exit()
   		elif opt in ("-i", "--ifile"):
   			inputfile = arg
   		elif opt in ("-o", "--ofile"):
   			outputfile = arg
   AnalyseFolder(inputfolder)

#save dataframe DF to a csv
def SaveDFToCSV(df, path):
	print("save to csv "+path)
	try:
		df.to_csv(path, encoding='utf-8', index=False)
	except ValueError:
		print("Can't save df")

#search a folder for files, and apply the analysefile method on each file.
def AnalyseFolder(path):
	thisPath = path
	for file in os.listdir(path):
		filePath = os.path.join(path,file)
		print("Analyse: "+ filePath)
		AnalyseFile(filePath)

#run a few different methods on the file such as
#RequestOCRPRocessing to return the text found in an image
#SearchDataForDecimal to return any text that looks like it may be a price
#SearchForDescription to return anything that looks like it may help describe what the reciept was for
#SearchForDate to return anything that looks like a date
#<TODO> improve the contrast on the image using openCV. some reciepts are not having all the text picked up
#<TODO> find the vendor based on a dict of known vendors
#<TODO> Itemise the purchases and somehow save those
#<TODO> Validate the total price. It is making some big assumptions that the total is the highest decimal number found which isn't always the case
def AnalyseFile(path):
	showResult = True
	thisUrl = path
	#"https://media-cdn.tripadvisor.com/media/photo-s/0f/12/7d/69/bill-for-2-april-2017.jpg"    
	requestData = Reciept.RequestOCRProcessing(thisUrl,showResult)
	priceList = Reciept.SearchDataForDecimal(requestData)
	descriptionList = Reciept.SearchForDescription(requestData)
	highestPrice = Reciept.GetHighest(priceList)
	date = Reciept.SearchForDate(requestData)
	date = date[0]

	ccType = Reciept.SearchForCCType(requestData)
	ccType = ''.join(ccType)

	priceData = [[date,path,descriptionList,ccType,highestPrice]]

	df = pd.DataFrame(priceData, columns=['Date','FileName','Description','CCType','Total'])
	#convert the list to be a string
	df['Description'] = df['Description'].apply(lambda x: ','.join(map(str, x)))
	#print(priceList)

	csvFileName = 'RecieptRecord.csv'
	if(os.path.exists(csvFileName)):
		appendedDF = pd.read_csv('RecieptRecord.csv')
		#pd.concat([appendedDF,df])
		newDF = appendedDF.append(df, sort=False)
	else:
		print("No csv exisits")
		newDF = df
	if(showResult):
		print(str(date)+' | '+ str(ccType) + ' | '+ str(highestPrice))
	SaveDFToCSV(newDF, csvFileName)


if __name__ == "__main__":
   main(sys.argv[1:])
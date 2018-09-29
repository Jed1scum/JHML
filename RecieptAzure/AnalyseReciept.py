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

def SaveDFToCSV(df, path):
	print("save to csv "+path)
	try:
		df.to_csv(path, encoding='utf-8', index=False)
	except ValueError:
		print("Can't save df")

def AnalyseFolder(path):
	thisPath = path
	for file in os.listdir(path):
		filePath = os.path.join(path,file)
		print("Analyse: "+ filePath)
		AnalyseFile(filePath)


def AnalyseFile(path):

	thisUrl = path
	#"https://media-cdn.tripadvisor.com/media/photo-s/0f/12/7d/69/bill-for-2-april-2017.jpg"    
	requestData = Reciept.RequestOCRProcessing(thisUrl,False)

	priceList = Reciept.SearchDataForDecimal(requestData)
	descriptionList = Reciept.SearchForDescription(requestData)

	highestPrice = Reciept.GetHighest(priceList)
	date = datetime.datetime.now()

	priceData = [[date,path,descriptionList,highestPrice]]

	df = pd.DataFrame(priceData, columns=['Date','FileName','Description','Total'])
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

	SaveDFToCSV(newDF, csvFileName)


if __name__ == "__main__":
   main(sys.argv[1:])
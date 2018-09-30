import Reciept

#This test suit is used to test the Reciept utility methods to ensure they are robust
thisUrl = "https://d85ecz8votkqa.cloudfront.net/support/help_center/Receipt_With_Signature_Line.JPG"
#"https://media-cdn.tripadvisor.com/media/photo-s/0f/12/7d/69/bill-for-2-april-2017.jpg"    
requestData = Reciept.RequestOCRProcessing(thisUrl,True)

#dateData = Reciept.SearchForDate(requestData)[0]
ccData = Reciept.SearchForCCType(requestData)
print(ccData)
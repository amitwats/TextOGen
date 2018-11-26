import csv
import pandas
import numpy
import sys

def ReadStringOfFile(fileName):
	with open (fileName, "r") as myfile:
		data=myfile.read()
	return data


def GetEndOfParamIndex(str,indexToSearchFrom):
	MAX_INDEX=1000000
	lastIndex=MAX_INDEX
	indexList=" ,().#"
	for i in range(0,len(indexList)):
		index= str.find(indexList[i:i+1],indexToSearchFrom+1)
		
		if index!=-1:
			lastIndex=(lastIndex,index)[index<lastIndex]

	retIndex=(lastIndex,-1)[lastIndex==MAX_INDEX]
	return retIndex


#Returns all the parametrers expected in the string
def GetListOfParams(str):
	listParams=[]
	isNextParam=True
	hashIndex=0
	while isNextParam:
		hashIndex=str.find("#",hashIndex)
		if hashIndex!=-1:
			endParamIndex= GetEndOfParamIndex(str,hashIndex)
			if endParamIndex==-1:
				endParamIndex=len(str)+1
			paramString=str[hashIndex+1:endParamIndex]
			listParams.append(paramString)
			hashIndex=hashIndex+1
		else:
			break
	return set(listParams);


#s=" This is a #test string to #see ahat parameters we #have and what can be done. Now to #test is #duplicate values are #included If we #see #duplicate values we need to #rewrite"

if __name__ == "__main__":

	input_template_file=sys.argv[1]  #template file
	input_parameter_file=sys.argv[2] # parameter file


	s=ReadStringOfFile(input_template_file)
	df = pandas.read_csv(input_parameter_file)
	listParams=GetListOfParams(s)
	for index, row in df.iterrows():
		outputString=s
		for param in listParams:
			cellValue=row[param]
			if cellValue!=df.isnull().any().any():
				outputString=outputString.replace("#"+param,str(cellValue))
		print( outputString)


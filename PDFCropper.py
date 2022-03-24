import numpy
from PyPDF2 import PdfFileReader, PdfFileWriter

def cropPageLeft(page):
	width = page.mediaBox.lowerRight[0]
	height = page.mediaBox.upperLeft[1]
	
	page.cropBox.lowerLeft = (0, height/2)
	page.cropBox.lowerRight = (width, height/2)
	page.cropBox.upperLeft = (0, height)
	page.cropBox.upperRight = (width, height)

def cropPageRight(page):
	width = page.mediaBox.lowerRight[0]
	height = page.mediaBox.upperLeft[1]
	
	page.cropBox.lowerLeft = (0, 0)
	page.cropBox.lowerRight = (width, 0)
	page.cropBox.upperLeft = (0, height/2)
	page.cropBox.upperRight = (width, height/2)

def splitPDF(pdf, pagesPerDocument):
	reader1 = PdfFileReader(pdf)
	reader2 = PdfFileReader(pdf)
	numPages = reader1.getNumPages()
	
	if numPages % pagesPerDocument != 0:
		raise Exception(f"Number of pages not divisible by {pagesPerDocument}.")
		
	numDocs = numPages // pagesPerDocument
	
	pages1 = [reader1.getPage(i) for i in range(numPages)]
	pages2 = [reader2.getPage(i) for i in range(numPages)]
	
	arraysOfPages1 = numpy.array_split(pages1, numDocs)
	arraysOfPages2 = numpy.array_split(pages2, numDocs)
	
	writers = []
	
	for i in range(numDocs):
		writer = PdfFileWriter()
		
		for j in range(pagesPerDocument):
			cropPageLeft(arraysOfPages1[i][j])
			cropPageRight(arraysOfPages2[i][j])
			
			if j % 2 == 0:
				writer.insertPage(arraysOfPages1[i][j])
				writer.addPage(arraysOfPages2[i][j])	
			if j % 2 == 1:
				writer.addPage(arraysOfPages1[i][j])
				writer.insertPage(arraysOfPages2[i][j])	
	
		writers.append(writer)
	
	return writers

pagesPerDocument = int(input("Enter number of pages per document: "))
	

with open("PDF.pdf", "rb") as input:
	writers = splitPDF(input, pagesPerDocument)
	outputWriter = PdfFileWriter()
	
	for writer in writers:
		for page in [writer.getPage(i) for i in range(writer.getNumPages())]:
			outputWriter.addPage(page)
			
		
	with open("output.pdf", "wb") as output:
		outputWriter.write(output)
		
					

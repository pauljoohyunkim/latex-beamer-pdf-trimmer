import sys
import os
import difflib
import pickle
import PyPDF2

class ConsecutivePageDifference:
    def __init__(self, pages: PyPDF2.PdfReader.pages):
        self.pages = pages
        self.page1 = None
        self.page2 = None
        self.str1 = None
        self.str2 = None
        self.stringmatches = None
        self.headerlength = 0
        self.footerlength = 0
    
    def setPagePair(self, pagenum):
        self.page1 = self.pages[pagenum]
        self.page2 = self.pages[pagenum+1]
        self.str1 = self.page1.extract_text()
        self.str2 = self.page2.extract_text()
        self.stringmatches = difflib.SequenceMatcher(None, self.str1, self.str2).get_matching_blocks()
        self.getCommonHeaderLength()
        self.getCommonFooterLength()
        
    def getCommonHeaderLength(self) -> None:
        if self.stringmatches:
            if self.stringmatches[0].a == 0 and self.stringmatches[0].b == 0:
                self.headerlength = self.stringmatches[0].size
                return
        self.headerlength = 0
    
    def getCommonFooterLength(self) -> None:
        # Reverse the string and find footer
        reversed_str1 = self.str1[::-1]
        reversed_str2 = self.str2[::-1]
        headerdetector = difflib.SequenceMatcher(None, reversed_str1, reversed_str2).get_matching_blocks()
        if headerdetector:
            if headerdetector[0].a == 0 and headerdetector[0].b == 0:
                self.footerlength = headerdetector[0].size
                return
        self.footerlength = 0
    
    def isContentAdded(self) -> bool:
        '''
        Returns whether the next slide is acquired from adding some more text.
        '''
        page1_text_without_header_and_footer = self.str1[self.headerlength: -self.footerlength + len(self.str1)].strip()
        page2_text_without_header_and_footer = self.str2[self.headerlength: -self.footerlength + len(self.str2)].strip()
        return page1_text_without_header_and_footer in page2_text_without_header_and_footer

class PDFAnalyzer:
    def __init__(self, readerObj : PyPDF2.PdfReader):
        self.readerObj = readerObj

    def getDiscardPageNums(self) -> set:
        reader = self.readerObj
        consecutiveAnalyzer = ConsecutivePageDifference(reader.pages)

        discardPageNums = set()
        pdfPageNum = len(reader.pages)
        for pagenum in range(pdfPageNum - 1):
            consecutiveAnalyzer.setPagePair(pagenum)
            if consecutiveAnalyzer.isContentAdded():
                discardPageNums.add(pagenum)
            print(f"Progress (Analyzer): {pagenum} / {pdfPageNum}", end="\r")
        
        print(f"Pages to discard: {discardPageNums}")
        return discardPageNums

class PDFRecompiler:
    def __init__(self, outputfilename : str, reader : PyPDF2.PdfReader):
        self.writer = PyPDF2.PdfWriter()
        self.reader = reader
        self.outputfilename = outputfilename
    
    def compile(self, discardPageNums : set):
        num_of_pages = len(self.reader.pages)
        for i in range(num_of_pages):
            if i not in discardPageNums:
                try:
                    self.writer.add_page(self.reader.pages[i])
                    print(f"Progress (Recompiler): {i} / {num_of_pages}", end="\r")
                except AttributeError:
                    sys.stderr.write(f"There seems to be a problem of missing attributes. Try repairing the pdf.\n")
                    sys.exit(2)
        self.writer.write(self.outputfilename)
        print(f"Done! Check the file at {self.outputfilename}.")


if __name__ == "__main__":
    argc = len(sys.argv)
    inputfilename = ""
    outputfilename = ""

    # If no argument
    if argc == 1:
        print(f"Usage: {os.path.basename(__file__)} (input.pdf) [output.pdf]")
        sys.exit(1)
    
    # If one argument
    if argc == 2:
        inputfilename = sys.argv[1]
        ifilename, ifilename_ext = os.path.splitext(inputfilename)
        outputfilename = f"{ifilename}_trimmed{ifilename_ext}"
        print(f"Input file: {inputfilename}")
        print(f"Output file: {outputfilename}")
    if argc == 3:
        inputfilename = sys.argv[1]
        outputfilename = sys.argv[2]
        print(f"Input file: {inputfilename}")
        print(f"Output file: {outputfilename}")
    
    # Read pdf file
    reader = PyPDF2.PdfReader(inputfilename)

    # Check if pickle file exists.
    # If there is, use the pickle file instead of analyzing from the beginning
    discardPageNumsFilename = f"{os.path.splitext(inputfilename)[0]}_temp.pkl"
    if os.path.isfile(discardPageNumsFilename):
        print(f"{discardPageNumsFilename} exists. Skipping analysis and using this instead.")
        with open(discardPageNumsFilename, "rb") as file:
            discardPageNums = pickle.load(file)
    else:
        analyzer = PDFAnalyzer(reader)
        discardPageNums = analyzer.getDiscardPageNums()
        with open(discardPageNumsFilename, "wb") as file:
            pickle.dump(discardPageNums, file)
        print(f"{discardPageNumsFilename} created. If there is an error in the compilation process, you could skip analysis by keeping this file.")

    # Write pdf file
    recompiler = PDFRecompiler(outputfilename, reader)
    recompiler.compile(discardPageNums)
import sys
import os
import difflib
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
    consecutiveAnalyzer = ConsecutivePageDifference(reader.pages)

    discardPageNums = set()
    for pagenum in range(len(reader.pages) - 1):
        consecutiveAnalyzer.setPagePair(pagenum)
        if consecutiveAnalyzer.isContentAdded():
            discardPageNums.add(pagenum)
    
    print(f"Pages to discard: {discardPageNums}")

    # Write pdf file
    writer = PyPDF2.PdfWriter()
    for i in range(len(reader.pages)):
        if i not in discardPageNums:
            writer.add_page(reader.pages[i])
    writer.write(outputfilename)
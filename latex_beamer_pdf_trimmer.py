import sys
import os
import difflib
import PyPDF2

class ConsecutivePageDifference:
    def __init__(self, page1: PyPDF2.PageObject, page2: PyPDF2.PageObject):
        self.page1 = page1
        self.page2 = page2
        self.str1 = page1.extract_text()
        self.str2 = page2.extract_text()
        self.stringmatches = difflib.SequenceMatcher(None, self.str1, self.str2).get_matching_blocks()
        
    def isThereCommonHeader(self) -> bool:
        if self.stringmatches:
            if self.stringmatches[0].a == 0 and self.stringmatches[0].b == 0:
                return True
        return False


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
    # There might be common substrings in each page, which might needs detection.
    # A potential method is to find the longest common substrings, then see if they needs disregardment.
    reader = PyPDF2.PdfReader(inputfilename)
    page = reader.pages[0]
    print(page.extract_text())

    

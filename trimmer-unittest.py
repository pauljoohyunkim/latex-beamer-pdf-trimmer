import unittest
import PyPDF2
import latex_beamer_pdf_trimmer

class TestPageComparison(unittest.TestCase):

    def test_common_header(self):
        reader = PyPDF2.PdfReader("tests/pres1.pdf")
        pages = list(reader.pages)
        analyzer = latex_beamer_pdf_trimmer.ConsecutivePageDifference(pages)
        analyzer.setPagePair(0)
        self.assertFalse(analyzer.isThereCommonHeader())
        analyzer.setPagePair(1)
        self.assertTrue(analyzer.isThereCommonHeader())

#    def test_common_footer(self):
#        reader = PyPDF2.PdfReader("tests/pres1.pdf")
#        pages = list(reader.pages)
#        consecutive_analysis1 = latex_beamer_pdf_trimmer.ConsecutivePageDifference(pages[0], pages[1])
#        self.assertFalse(consecutive_analysis1.isThereCommonFooter())
#        consecutive_analysis2 = latex_beamer_pdf_trimmer.ConsecutivePageDifference(pages[1], pages[2])
#        self.assertTrue(consecutive_analysis2.isThereCommonFooter())
        

if __name__ == "__main__":
    unittest.main()
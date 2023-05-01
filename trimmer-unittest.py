import unittest
import PyPDF2
import latex_beamer_pdf_trimmer

class TestPageComparison(unittest.TestCase):

    def test_common_header(self):
        reader = PyPDF2.PdfReader("tests/pres1.pdf")
        pages = list(reader.pages)
        analyzer = latex_beamer_pdf_trimmer.ConsecutivePageDifference(pages)
        analyzer.setPagePair(0)
        self.assertEqual(analyzer.headerlength, 0)
        analyzer.setPagePair(1)
        self.assertGreater(analyzer.headerlength, 0)

    def test_common_footer(self):
        reader = PyPDF2.PdfReader("tests/pres1.pdf")
        pages = list(reader.pages)
        analyzer = latex_beamer_pdf_trimmer.ConsecutivePageDifference(pages)
        analyzer.setPagePair(0)
        self.assertEqual(analyzer.footerlength, 4)
        analyzer.setPagePair(1)
        self.assertGreater(analyzer.footerlength, 4)
        
        

if __name__ == "__main__":
    unittest.main()
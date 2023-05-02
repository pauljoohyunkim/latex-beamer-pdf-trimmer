# latex-beamer-pdf-trimmer
A script to cut down on redundant slides from animation

## Usage:
```
$ python latex_beamer_pdf_trimmer.py (input_file.pdf) [output_file.pdf]
```
If output_file.pdf is not provided, by default it will be assigned input_file_**trimmed**.pdf.

Try a demo by:
```
$ python latex_beamer_pdf_trimmer.py tests/pres1.pdf ./pres1_trimmed.pdf
```
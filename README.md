# latex-beamer-pdf-trimmer
A script to cut down on redundant slides from animation

## Dependency
You need PyPDF2 module before using this program.
You can install by:
```
$ pip install PyPDF2
```
Or you can try this program without installing the module into your system by creating a virtual environment.
```
# Create virtual environment called "venv"
python -m venv venv     

# If you are using Linux,
source venv/bin/activate
# If you are using Windows,
venv/Scripts/activate.bat

# Install PyPDF2 dependency on the virtual environment.
pip install -r requirements.txt
```

## Usage:
```
$ python latex_beamer_pdf_trimmer.py (input_file.pdf) [output_file.pdf]
```
If output_file.pdf is not provided, by default it will be assigned input_file_**trimmed**.pdf.

If you have **make** installed, try a demo by:
```
$ make demo
```
Otherwise run the demo manually by:
```
$ python latex_beamer_pdf_trimmer.py tests/pres1.pdf ./pres1_trimmed.pdf
```
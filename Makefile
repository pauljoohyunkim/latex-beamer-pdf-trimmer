
test: trimmer-unittest.py
	python -m unittest -v $<

demo: latex_beamer_pdf_trimmer.py tests/pres1.pdf
	python $^

tests/pres1.pdf: tests/pres1.tex
	pdflatex -output-directory tests $^

clean:
	$(RM) tests/pres1_trimmed.pdf
help:
	@echo " * clean     : Delete temporary files"
	@echo " * all       : Create the PDF file (run everything needed)"
	@echo " * full      : Create the PDF file (run LaTeX and BibTeX only)"
	@echo " * quicker   : Update the PDF file (just run LaTeX twice)"
	@echo " * quick     : Update the PDF file (just run LaTeX once)"
	@echo " * bib       : Update the bib file (just run BibTeX/biber once)"
	@echo " * bibchk    : Run some checks (e.g. biber, bibtex-check)"
	@echo " * verify    : Run some checks (e.g. l2tabu)"
	@echo " * spell     : Check for spelling errors (aspell)"
	@echo " * eval      : Run evaluation scripts (e.g. R)"
	@echo " * generate  : Generate images (gnuplot, R, dot/graphviz, ...)"
	@echo " * deploy    : Deploy the PDF file to a directory (e.g. for automated builds)"
	@echo " * update    : Get the latest sources (incl. latest library)"
	@echo " * open      : Opens the output file using 'open'"
	@echo " * ci        : Continuous Integration - watch for changes an rebuild everything"
	@echo " * rename    : Rename project"
	@echo " * unicode   : Find incompatible unicode characters"
	@echo " * optimize  : Optimize output (e.g. optipng)"
	@echo " * sign      : Sign the PDF using an X.509 certificate"
	@echo " * preflight : Test for PDF/A and PDF/X compatibility"
	@echo " * fix       : Give some hints on how to fix the current setup"
	@echo " * todo      : Find open todos"

todo:
	@find . -iname "*.tex" -exec sh -c "grep -Hin 'TODO{' {}|sed 's/^\(.*\):\(.*\):.*{\(.*\)}/ * TODO \"\3\" in file \1 in line \2/'" \;

clean:
	@./build.sh -c

all: generate
	@./build.sh -b

full:
	@./build.sh -b

quick:
	@./build.sh -q

quicker:
	@./build.sh -r

bib:
	@./build.sh -i

bibchk:
	@./build.sh -w

verify:
	@./build.sh -v

spell:
	@./build.sh -s

eval:
	@./build.sh -e

generate:
	@./build.sh -g

open:
	@./build.sh -o

deploy:
	@./build.sh -d ${DPATH}

ci:
	@./build.sh -f

unicode:
	@./build.sh -u

optimize:
	@./build.sh -z

sign:
	@./build.sh -x

preflight:
	@./build.sh -p

rename:
	@./build.sh -n

fix:
	@echo 'You should run: rm -rf $$(biber --cache)'

update:
	@git submodule foreach git pull origin master
	@git pull

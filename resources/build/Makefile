help:
	@echo " * clean   : Delete temporary files"
	@echo " * build   : Create the PDF file (run everything needed)"
	@echo " * quick   : Update the PDF file (just run LaTeX once)"
	@echo " * verify  : Run some checks (e.g. l2tabu)"
	@echo " * spell   : Check for spelling errors (aspell)"
	@echo " * eval    : Run evaluation scripts (e.g. R)"
	@echo " * generate: Generate images (gnuplot, R, dot/graphviz, ...)"

clean:
	@./build.sh -c

build: generate
	@./build.sh -b

quick:
	@./build.sh -q

verify:
	@./build.sh -v

spell:
	@./build.sh -s

eval:
	@./build.sh -e

generate:
	@./build.sh -g

###############################################################################
# FILE: Makefile
#
# Author: Dan Whitman
##############################################################################

.PHONY: all clean board her help

ODIR=output

#==============================================================================
all: board her him tree
#==============================================================================

#==============================================================================
help:
#==============================================================================
	@echo "all:		Build the manual from the LaTeX source code."
	@echo "clean:		Remove all of the build files for the PDFs."
	@echo "board:		Build game board PDF."
	@echo "tree:		Build game tree PDF."
	@echo "her:		Build the positions and moves for a HER, the black player."
	@echo "him:		Build the positions and moves for a HIM, the white player."

#==============================================================================
board:
#==============================================================================
	mkdir -p ${ODIR}
	cp board.tex ${ODIR}
	cd ${ODIR}; pdflatex board.tex

#==============================================================================
her:
#==============================================================================
	mkdir -p ${ODIR}
	./build-positions.py > ${ODIR}/her.tex
	cd ${ODIR}; pdflatex her.tex

#==============================================================================
him:
#==============================================================================
	mkdir -p ${ODIR}
	./build-positions.py -i > ${ODIR}/him.tex
	cd ${ODIR}; pdflatex him.tex

#==============================================================================
tree:
#==============================================================================
	mkdir -p ${ODIR}
	./build-tree.py > ${ODIR}/tree.tex
	cd ${ODIR}; lualatex tree.tex
	plakativ --pagesize A3 --output=${ODIR}/tree_poster.pdf --maxpages 4 ${ODIR}/tree.pdf

#==============================================================================
clean:
#==============================================================================
	-rm -r -f __pycache__ ${ODIR}

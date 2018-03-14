NAME := binary-tree
PYTHON := python

test: $(NAME).png
	display $<

$(NAME).png: $(NAME).dot
	dot -Tpng -o $@ $<

$(NAME).dot: __main__.py $(NAME).input
	$(PYTHON) $< < $(NAME).input > $@

clean:
	git clean -x -d -f

.PHONY: clean test

# $@ - current target
# $* '%'-part (works if there *is* '%' in specification)
# $< first dependence
# $^ all dependencies (without duplicates)

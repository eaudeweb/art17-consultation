LESS_FILES= art17/static/style.less
CSS_FILES=$(LESS_FILES:.less=.css)

less: $(CSS_FILES)

%.css: %.less
	lessc -x $< $@

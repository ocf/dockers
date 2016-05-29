.PHONY: build
build:
	./template.py

.PHONY: push
push:
	./template.py --push

.PHONY: clean
clean:
	find . -mindepth 1 -maxdepth 1 -type d ! -name include ! -name '.git*' -print0 | \
	xargs -0 rm -r

.PHONY: build
build:
	./template.py

.PHONY: test
test: build
	./test.sh

.PHONY: clean
clean:
	find . -mindepth 1 -maxdepth 1 -type d ! -name include ! -name '.git*' -print0 | \
	xargs -0 rm -r

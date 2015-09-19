.PHONY: Dockerfiles
Dockerfiles:
	for tag in wheezy jessie stretch sid; do \
		mkdir -p "$$tag"; \
		sed "s/{tag}/$$tag/" Dockerfile.in | sed "/# no:$$tag/d" | sed 's/\s*#.*$$//' > "$$tag/Dockerfile"; \
	done

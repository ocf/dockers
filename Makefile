.PHONY: Dockerfiles
Dockerfiles:
	for tag in wheezy jessie squeeze sid; do \
		mkdir -p "$$tag"; \
		sed "s/{tag}/$$tag/" Dockerfile.in > "$$tag/Dockerfile"; \
	done

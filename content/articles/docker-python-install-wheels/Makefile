.PHONY: build-break
build-break:
	docker build -t blog-python:break -f ./Dockerfile.break .

.PHONY: build-big
build-big:
	docker build -t blog-python:big -f ./Dockerfile.big .
	docker images

.PHONY: build-uninstall-big
build-uninstall-big:
	docker build -t blog-python:big-uninstall -f ./Dockerfile.uninstall .
	docker images

.PHONY: build-small
build-small:
	docker build -t blog-python:small -f ./Dockerfile.small .
	docker images

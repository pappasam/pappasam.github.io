GITHUB_PAGES_BRANCH=master

.PHONY: help
help:  ## Print this help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: setup
setup: clone-themes
	poetry install

.PHONY: serve
serve:  build-dev  ## Run a local development server
	pelican --listen --relative-urls

.PHONY: publish
publish: build-publish  ## Publish the website to Github Pages
	ghp-import \
		--message="Generate Pelican site" \
		--branch=$(GITHUB_PAGES_BRANCH) \
		--cname="samroeca.com" \
		output
	git push origin $(GITHUB_PAGES_BRANCH)

.PHONY: build-dev
build-dev:  ## Build a static, development version of the website
	pelican --settings pelicanconf.py content

.PHONY: build-publish
build-publish:  ## Build a static, production version of the website
	pelican --settings publishconf.py content

.PHONY: clone-themes
clone-themes:  ## Clone relevant themes to ./pelican-themes
	git clone git@github.com:pappasam/Flex.git pelican-themes/Flex

.PHONY: clean
clean:  ## Remove the output directory
	rm -r output
	rm seo_report.html

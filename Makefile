INPUTDIR=$(CURDIR)/content
OUTPUTDIR=$(CURDIR)/output
CONFFILE=$(CURDIR)/pelicanconf.py
PUBLISHCONF=$(CURDIR)/publishconf.py
GITHUB_PAGES_BRANCH=master

.PHONY: help
help:  ## Print this help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: setup
setup: clone-themes
	poetry install

.PHONY: clean
clean:  ## Remove the output directory
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

.PHONY: serve
serve:  build-dev  ## Run a local development server
	pelican --listen --relative-urls

.PHONY: publish
publish: build-publish  ## Publish the website to Github Pages
	ghp-import \
		--message="Generate Pelican site" \
		--branch=$(GITHUB_PAGES_BRANCH) \
		--cname="samroeca.com" \
		$(OUTPUTDIR)
	git push origin $(GITHUB_PAGES_BRANCH)

.PHONY: build-dev
build-dev:  ## Build a static, development version of the website
	pelican $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE)

.PHONY: build-publish
build-publish:  ## Build a static, production version of the website
	pelican $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF)

.PHONY: clone-themes
clone-themes:  ## Clone relevant themes to ./pelican-themes
	git clone git@github.com:alexandrevicenzi/Flex.git pelican-themes/Flex

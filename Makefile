INPUTDIR=$(CURDIR)/content
OUTPUTDIR=$(CURDIR)/output
CONFFILE=$(CURDIR)/pelicanconf.py
PUBLISHCONF=$(CURDIR)/publishconf.py
GITHUB_PAGES_BRANCH=master

.PHONY: build
build: html

.PHONY: html
html:
	pelican $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE)

.PHONY: clean
clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

.PHONY: serve
serve:
	pelican --listen --relative-urls

.PHONY: publish
publish:
	pelican $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF)

.PHONY: github
github: publish
	ghp-import \
		--message="Generate Pelican site" \
		--branch=$(GITHUB_PAGES_BRANCH) \
		--cname="softwarejourneyman.com" \
		$(OUTPUTDIR)
	git push origin $(GITHUB_PAGES_BRANCH)

.PHONY: clone_themes
clone_themes:
	git clone --recursive git@github.com:getpelican/pelican-themes.git

.PHONY: clone_plugins
clone_plugins:
	git clone --recursive git@github.com:getpelican/pelican-plugins.git

.PHONY: clone_github_page
clone_github_page:
	git clone git@github.com:pappasam/pappasam.github.io.git output

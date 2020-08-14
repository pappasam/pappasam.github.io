---
title: How to write a coc.nvim plugin
date: 2020-08-14
category: Software Development
modified: 2020-08-14
tags: Vim, Vim Plugins
---

**draft: subject to change**

In this post, I build a `coc.nvim` plugin that wraps an executable language server. By the end of this article, you should be able to write your own MVP coc plugin to wrap any executable language server.

<!-- PELICAN_END_SUMMARY -->

## Background

[coc.nvim](https://github.com/neoclide/coc.nvim), short for "conquer of completion", is an [lsp](https://microsoft.github.io/language-server-protocol/overviews/lsp/overview/) client that targets [Vim](https://www.vim.org/). Vim (in my case, technically [NeoVim](https://neovim.io)) is my favorite text editor / IDE. I like its extensibility, flexibility, and in-terminal slickness. Over the years, plenty of tooling/plugins have been built for Vim that make it easy to program in multiple languages. Here are some examples:

- JavaScript intellisense: [tern_for_vim](https://github.com/ternjs/tern_for_vim)
- Ruby on rails intellisense: [vim-rails](https://github.com/tpope/vim-rails)
- General linting: [syntastic](https://github.com/vim-syntastic/syntastic)
- Python intellisense: [jedi-vim](https://github.com/davidhalter/jedi-vim)

Vim's diverse plugins and community-supported tooling are what first drew me to the editor, and they're what still keep me here. Sadly for me, not all software developers use Vim. See its share of developers from the [2019 StackOverflow developer survey](https://insights.stackoverflow.com/survey/2019#technology-_-most-popular-development-environments):

![stack overflow survey](./images/coc-plugin/so-2019-dev-env.png)

Popular editors (and platforms) tend to have more software developed for them. For example, many developers have historically targeted Windows **for its users**, not because they [like writing code on Windows](https://www.quora.com/Why-do-computer-programmers-love-Linux-and-hate-Windows). Mo' people, mo' software. To further complicate things, different programming languages tended to be popular with different editors: Vim's Java development environment was historically abysmal enough to generate some [heated conversations](https://news.ycombinator.com/item?id=9713478) concluding that only the most obstinate, impractical developers would even consider it for Java development.

This sad historical reality kept language tooling development isolated to editors that were popular within a language: PyCharm/Vim for Python, [Eclipse](https://www.eclipse.org/eclipseide/) for Java, etc. This, in turn, would force developers into mind-bending context switches when changing languages. Not only would we need to learn a new language, we'd also need to learn a whole new text editor and tooling ecosystem! Since software tooling is somewhat of a religion, there was no way you could get some developers (eg, me) to even consider touching Java if I had to sacrifice my beliefs (Vim/development tooling I'd grown accustomed to).

In 2015/2016, when things seemed most dire and intractible, the developers behind VSCode had a big idea: why don't we abstract all this divergent, isolated tooling into a [protocol](https://en.wikipedia.org/wiki/Communication_protocol) that generalizes the problem of language tooling. Thus, the language server protocol was born.

### Language Server Protocol

The "Language Server Protocol" (LSP) is a specification that describes communication between a "language client" and a "language server". The following definitions are appropriated from the [lsp spec overview](https://microsoft.github.io/language-server-protocol/overviews/lsp/overview/):

- **Language server:** a program that contains language-specific "smarts" that can communicate with development tooling through the LSP
- **Language client:** a program, developed in the environment of a "development tool", that can send, receive, and act on LSP messages with a "language server"
- **Development tool:** Vim, Neovim, VS Code, Eclipse, etc. Basically, a text editor or IDE that software developers use to develop software

![Language Server Protocol](https://microsoft.github.io/language-server-protocol/overviews/lsp/img/language-server-sequence.png)

Above, the language client is sitting in the development tool and sending [JSON-RPC](https://en.wikipedia.org/wiki/JSON-RPC) requests to a language server. All this basically means that your text editor is asking something that knows way more about your programming language (Python) than your text editor and responding to its suggested actions. These actions may range from "you should autocomplete some text" to "this symbol's definition can be found by opening this file and navigating to this precise position). In short, the orchestrated communication outlined above realizes the following dream:

1. Language tooling developers write 1 program (the language server) to target every development tool (Vim, VS Code, etc)
2. Development tool developers write 1 program (the language client) that knows how to communicate with all language servers
3. Software developers have first-class language support for all languages in their favorite editor; no more text-editor context switching!

The above dream seemed like it would herald a new dawn for developers: we can all happily use our favorite tools and have similar language support! Unfortunately, VSCode's popularity has made things a bit more complicated in 2020...

### VSCode: client power

The LSP dream described in the previous section was similar to [Tim Berners-Lee](https://en.wikipedia.org/wiki/Tim_Berners-Lee)'s dream for a world wide web: web clients, supporting web protocols, could enable communication between web servers and a user environment (the operating system). This dream sparked development of all sorts of web clients (browsers) and culminated in the [first browser war](https://en.wikipedia.org/wiki/Browser_wars). According to Wikipedia, during this time, Netscape Navigator and Internet Explorer implemented proprietary html tags like `<blink>` for Navigator and `<marquee>` for Internet Explorer. They also rapidly developed their own features and began diverging from [W3C](https://en.wikipedia.org/wiki/World_Wide_Web_Consortium)'s recommended spec. This resulted in code that would run most-efficiently on one platform being less efficient or broken on the other. This forced users to pick browses based on custom compatibility with their favorite sites and ultimately resulted in [United States v. Microsoft Corp](https://en.wikipedia.org/wiki/United_States_v._Microsoft_Corp.). Basically, things got ugly.

Although what is happening today in the text editing community is tamer, it resembles the first browser war because VSCode has become the de-facto standard for Language Clients. Authors of Language Servers may target VSCode without fully supporting the current LSP spec or by inadvertently support VSCode features that are not in the spec. This means that [Atom](https://atom.io/) users might be using a correctly-implemented language client that does not work with certain language servers. Additionally, there may be no way to easily configure certain language servers without VSCode's configuration options. This means that if you want to get the best language support possible across all language servers, as of August 2020, you pretty much need to use something that resembles VSCode.

Luckily, [Qiming zhao](https://github.com/neoclide) and [Heyward Fann](https://github.com/fannheyward) realized that this problem could be solved for Vim by basically implementing a VSCode bridge for Neovim. They named this LSP bridge:

![coc](https://user-images.githubusercontent.com/251450/55009068-f4ed2780-501c-11e9-9a3b-cf3aa6ab9272.png)

### coc.nvim

[coc.nvim](https://github.com/neoclide/coc.nvim) is a language client for Vim that can be configured similarly to VSCode's language client. Vim is configured with [Vim script](https://en.wikipedia.org/wiki/Vim_%28text_editor%29#Vim_script), [C](https://en.wikipedia.org/wiki/C_%28programming_language%29), [lua](https://en.wikipedia.org/wiki/Lua_%28programming_language%29) (if using Neovim), and any other language if you're feeling fancy enough these days. VSCode is configured with [json](https://en.wikipedia.org/wiki/JSON) and [TypeScript](https://en.wikipedia.org/wiki/TypeScript). `coc.nvim` makes it so we can configure `coc.nvim`-managed features using `json` and `typescript` while still being able to use Vim's configuration for everything else. Basically, it's this:

![have your cake and eat it too](https://teflgeek.files.wordpress.com/2012/05/cake-and-eating-it-too.jpeg)

The rest of this article assumes that your development tool is Vim/Neovim and your language client is `coc.nvim`.

## Coc as simple LSP wrapper

Without a plugin, coc behaves like a simple language client. If you're using Neovim,

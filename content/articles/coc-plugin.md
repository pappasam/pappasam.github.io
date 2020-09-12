---
title: How to write a coc.nvim extension
date: 2020-08-14
category: Software Development
modified: 2020-08-14
tags: vim, neovim, lsp
summary: Build a "coc.nvim" extension that wraps an executable language server. You should learn what makes coc a stand-out LSP client and be able to write your own coc extension.
---

[TOC]

In this post, I build a "coc.nvim" extension that wraps an executable language server. By the end of this article, you should both understand what makes coc a stand-out LSP client and be able to write your own coc extension.

For the interactive parts of this post, you'll need the following:

- A POSIX-compliant terminal (bash, zsh, etc), or the ability to translate
- [git](https://git-scm.com/)
- [Node.js>=8.10.0](https://nodejs.org/en/)
- [yarn>=1.22.4](https://github.com/yarnpkg/yarn)
- [Vim 8+](https://github.com/vim/vim) or [Neovim 0.4.4+](https://github.com/neovim/neovim)
- [coc.nvim==0.0.78](https://github.com/neoclide/coc.nvim) (might work on newer versions, but no promises)
- Some knowledge of TypeScript might be helpful

Please disable Python-specific coc extensions ([coc-jedi](https://github.com/pappasam/coc-jedi), etc). Some terminology used throughout the post:

- Vim: Vim or Neovim
- vimrc: `~/.config/nvim/init.vim` for Neovim or `~/.vimrc` for Vim
- coc-settings.json: `~/.config/nvim/.coc-settings.json` by default

## Background

[coc.nvim](https://github.com/neoclide/coc.nvim), short for "conquer of completion", is an [lsp](https://microsoft.github.io/language-server-protocol/overviews/lsp/overview/) client that targets [Vim](https://www.vim.org/). Vim (or [NeoVim](https://neovim.io)) is my favorite text editor / IDE. I like its extensibility, flexibility, and in-terminal slickness. Vim has tools and plugins that make it easy to program in different programming languages. Here are some examples:

- JavaScript intellisense: [tern_for_vim](https://github.com/ternjs/tern_for_vim)
- Ruby on rails intellisense: [vim-rails](https://github.com/tpope/vim-rails)
- General linting: [syntastic](https://github.com/vim-syntastic/syntastic)
- Python intellisense: [jedi-vim](https://github.com/davidhalter/jedi-vim)

Vim's diverse plugins and community-supported tooling are what keep me coming back, but not all developers are like me. Visual Studio Code, Nodepad++, and others were more popular than Vim in the [2019 StackOverflow developer survey](https://insights.stackoverflow.com/survey/2019#technology-_-most-popular-development-environments):

![stack overflow survey](./images/coc-plugin/so-2019-dev-env.png)

These popularity differences are starker across programming language communities. For example, Vim's Java development environment was historically abysmal enough to generate some [heated conversations](https://news.ycombinator.com/item?id=9713478). My non-scientific evaluation of the community's sentiment: obstinate, impractical developers used Vim for Java development while practical, no-nonsense creators preferred Eclipse. Because of this sentiment, tooling for Java evolved in the Eclipse world while Vim's Java support remained neglected.

The Java pattern mentioned in the previous paragraph happens, to some extent, in all programming languages. Developers became drawn to editors best-supported their language of choice: PyCharm/Vim for Python, [Eclipse](https://www.eclipse.org/eclipseide/) for Java, [VSCode](https://code.visualstudio.com/) for TypeScipt/JavaScript, etc. This, in turn, forced developers into mind-bending context switches when changing languages. To become proficient with a new programming language, a developer needed to learn a whole new text editor and tooling ecosystem! Like asking a Jedi to use another Jedi's light saber, forcing a developer to learn and use [Emacs](https://en.wikipedia.org/wiki/Emacs) because it has better support for `<insert language here>` can evoke uncomfortable feelings (at best):

![Vi versus emacs cartoon](https://itsfoss.com/wp-content/uploads/2016/07/vi-emacs.png)

The rise of [full stack development](https://www.w3schools.com/whatis/whatis_fullstack.asp) and our general expectation that developers be comfortable writing code in more than one language made it so that by mid 2015, we seemed all-but doomed to a life of eternal context switching.

![broken bridge](https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Bridging_the_gap_%2825429796194%29.jpg/640px-Bridging_the_gap_%2825429796194%29.jpg)

When society was on the brink, the developers behind VSCode had a big idea: if we separate the tools that understand languages from the tools that edit text, and then give these separate tools a [communication protocol](https://en.wikipedia.org/wiki/Communication_protocol), this could enable Vim users to use the same language tools that power Eclipse and VSCode (and vise versa). They called this communication mechanism the "language server protocol".

![fixed bridge](https://s0.geograph.org.uk/geophotos/04/26/78/4267872_c1052b8a.jpg)

### Language Server Protocol

The "Language Server Protocol" (LSP) is a specification that describes communication between a "language client" and a "language server". The following definitions come from the [lsp spec overview](https://microsoft.github.io/language-server-protocol/overviews/lsp/overview/):

- **Language server:** a program that contains language-specific "smarts" that can communicate with development tooling through the LSP
- **Language client:** a program, developed in the environment of a "development tool", that can send, receive, and act on LSP messages with a "language server"
- **Development tool:** Vim, Neovim, VS Code, Eclipse, etc. Basically, a text editor or IDE that software developers use to develop software

![Language Server Protocol](https://microsoft.github.io/language-server-protocol/overviews/lsp/img/language-server-sequence.png)

Above, the language client is sitting in the development tool and sending [JSON-RPC](https://en.wikipedia.org/wiki/JSON-RPC) requests to a language server. All this basically means that your text editor is asking questions to an entity that knows way more about your programming language and responding to its suggested actions. These actions may range from "you should autocomplete some text" to "find this symbol's definition by opening this file and navigating to this precise position. In short, the orchestrated communication outlined above realizes the following dream:

1. Language tooling developers write 1 program (the language server) to target every development tool (Vim, VS Code, etc)
2. Development tool developers write 1 program (the language client) that knows how to communicate with all language servers
3. Software developers have first-class language support for all languages in their favorite editor; no more text-editor context switching!

The above dream seemed like it would herald a new dawn for developers: we can use our favorite tools and have similar, powerful programming language support! As the auguries looked good and a golden age seemed imminent, VSCode's popularity began generating some bad, familiar omens...

![black cat bad omen](https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Black_pussy_-_panoramio.jpg/640px-Black_pussy_-_panoramio.jpg)

### VSCode: client power

The LSP dream described in the previous section was similar to [Tim Berners-Lee](https://en.wikipedia.org/wiki/Tim_Berners-Lee)'s dream for a world wide web: web clients, supporting web protocols, could enable communication between web servers and a user environment (the operating system). This dream sparked development of all sorts of web clients (browsers) and culminated in the [first browser war](https://en.wikipedia.org/wiki/Browser_wars). According to Wikipedia, during this time, Netscape Navigator and Internet Explorer implemented proprietary html tags like `<blink>` for Navigator and `<marquee>` for Internet Explorer. They also rapidly developed their own features and began diverging from [W3C](https://en.wikipedia.org/wiki/World_Wide_Web_Consortium)'s recommended spec. This resulted in efficient Internet Explorer HTML being less efficient or broken on Navigator (and vise versa). This forced users to pick browsers based on custom compatibility with their favorite sites and ultimately resulted in [United States v. Microsoft Corp](https://en.wikipedia.org/wiki/United_States_v._Microsoft_Corp.). Basically, things got ugly.

![Browser wars](https://joaopsilva.github.io/talks/End-to-End-JavaScript-with-the-MEAN-Stack/img/ie-vs-netscape.jpg)

Although what is happening today in the text editing community is tamer, it resembles the first browser war in that VSCode has become the de-facto standard for Language Clients. Authors of Language Servers may target VSCode without fully supporting the current LSP spec or by inadvertently support VSCode features that are not in the spec. This means that [Atom](https://atom.io/) users might be using a correctly-implemented language client that does not work with certain language servers. Additionally, there may be no way to easily configure certain language servers without VSCode's configuration options. This means that if you want to get the best language support possible across all language servers, as of August 2020, you pretty much need to use something that resembles VSCode.

![you can't sit with us](https://memegenerator.net/img/instances/58875816/you-cant-sit-with-us.jpg)

As the VSCode ecosystem seemed like it had formed an exclusive clique, [Qiming zhao](https://github.com/chemzqm) (@chemzqm on social media) realized that Vim could join the party by [implementing a VSCode bridge for Neovim](https://news.ycombinator.com/item?id=19532429). Qiming zhao named this LSP bridge "coc.nvim".

![Python bridge](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Amsterdam_Python_Bridge_10.jpg/640px-Amsterdam_Python_Bridge_10.jpg)

## coc.nvim

[coc.nvim](https://github.com/neoclide/coc.nvim) is a language client for Vim that can be configured similarly to VSCode. Vim is configured with [Vim script](https://en.wikipedia.org/wiki/Vim_%28text_editor%29#Vim_script), [C](https://en.wikipedia.org/wiki/C_%28programming_language%29), [lua](https://en.wikipedia.org/wiki/Lua_%28programming_language%29) (if using Neovim), and any other language if you're feeling fancy enough these days. VSCode is configured with [json](https://en.wikipedia.org/wiki/JSON) and [TypeScript](https://en.wikipedia.org/wiki/TypeScript). "coc.nvim" makes it so we can configure "coc.nvim"-managed features using `json` and `typescript` while still being able to use Vim's configuration for everything else. Basically, it's this:

![have your cake and eat it too](https://teflgeek.files.wordpress.com/2012/05/cake-and-eating-it-too.jpeg)

### Register a language server

Without an extension, coc behaves like a simple language client. For simplicity's sake, let's assume we're all Python developers and that we'd like to use a language server named [jedi-language-server](https://github.com/pappasam/jedi-language-server) with Vim.

Within your current Python environment, install jedi-language-server:

```bash
pip install jedi-language-server
```

Now run jedi-language-server:

```bash
jedi-language-server
```

Notice that the process hangs; it's waiting to receive standard input and will respond with standard output. This server can run inside of Vim by placing the following code in the `languageserver` section of your coc-settings.json:

```json
{
  "languageserver": {
    "python": {
      "command": "jedi-language-server",
      "filetypes": ["python"]
    }
  }
}
```

If you've configured coc.nvim and installed jedi-language-server in an accessible location, Vim and jedi-language-server will communicate to provide you autocomletion, goto definition, etc. Hooray!

![message teamwork](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/A_message_written_on_rice_paper_is_put_into_a_container_and_attached_to_a_carrier_pigeon_by_members_of_61st_Division_Signals_at_Ballymena%2C_Northern_Ireland%2C_3_July_1941._H11281.jpg/612px-thumbnail.jpg)

#### Manual configuration

It turns out there are some practical problems with expecting users to configure jedi-language-server manually:

1. Remembering to manually install a language server can annoy people; shouldn't the editor remember to do that?
2. We'd like to configure the language server; can't that configuration have pretty autocompletion and look like the configuration I can use with all the other VSCode-like configuration options?
3. It's good UX to prevent preventable problems.

This is where coc extensions come into play: they avoid the above problems by providing default configurations and features. Users can seamlessly use a language server with an extension.

![extension](https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Europlug_extension_cord.jpg/640px-Europlug_extension_cord.jpg)

### Writing an extension

We will address 2 requirements in this post:

1. Prevent the user from needing to write manual configuration for jedi-language-server in coc-settings.json
2. Allow the user to configure the server as "disabled" if needed

The reader may address other requirements as a post-blog exercise.

#### Project skaffolding

In `~/src`, use [create-coc-extension](https://github.com/fannheyward/create-coc-extension) to create a project skeleton:

```console
$ yarn create coc-extension coc-jls
...
? Project title: coc-jls
? Project description: A great project
? Author full name: Your name
? Author email address: your.name@domain.com
? Initialize a git repository? Yes
? Install node dependencies? Yes
  installing node dependencies...
Done...
$ cd coc-jls
$ yarn
```

You should have the following version-controlled files in coc-jls:

```text
LICENSE
README.md
package.json
src/
  index.ts
  lists.ts
tsconfig.json
webpack.config.js
yarn.lock
```

Delete the files in `src`; we'll be writing these from scratch.

#### First file

To get a simple wrapper around an existing jedi-language-server executable, place the following code in `src/index.ts`:

```typescript
import { ExtensionContext, services, workspace, LanguageClient } from 'coc.nvim'

export async function activate(context: ExtensionContext): Promise<void> {
  const serverOptions = {
    command: 'jedi-language-server', // run jls
  }
  const clientOptions = {
    documentSelector: ['python'], // run jls on py files
  }
  const client = new LanguageClient(
    'coc-jls', // the id
    'coc-jls', // the name of the language server
    serverOptions,
    clientOptions
  )
  context.subscriptions.push(services.registLanguageClient(client))
}
```

This code tells coc to register a new language server named `coc-jls` that executes the command `jedi-language-server` when Vim edits Python file(s). Now build the project with the following command:

```bash
yarn

```

Open an empty file (test.py works) with Vim and run the following command:

```vim
:set runtimepath^=~/src/sandbox/coc-jls
```

This command will help coc discover your extension. Depending on your coc configuration, you should see diagnostics, have autocompletion, etc. In the long term, you may want to manage your coc extension as a plugin or a Vim [package](https://shapeshed.com/vim-packages), but we'll stay local and simple for now.

#### User configuration

We've wrapped jedi-language-server with a coc extension and now it's time to add some user configuration! Coc provides a simple mechanism to help users communicate their configuration values like VSCode: through the package.json. Make sure the following lines are in your package.json:

```json
{
  "contributes": {
    "configuration": {
      "type": "object",
      "title": "coc-jls configuration",
      "properties": {
        "coc-jls.enabled": {
          "type": "boolean",
          "default": true,
          "description": "Enable coc-jls extension"
        }
      }
    }
  }
}
```

This says that the coc-jls extension contributes a configuration key `coc-jls.enabled` whose default value is `true`. If a user wants to disable `coc-jls`, they must add the following line to the top level of coc-settings.json:

```json
{
  "coc-jls.enabled": false
}
```

Now we must add some logic to our typescript code to read the user configuration and disable the server if the user has chosen not to have it enabled:

```typescript
import { ExtensionContext, services, workspace, LanguageClient } from 'coc.nvim'

export async function activate(context: ExtensionContext): Promise<void> {
  // BEGIN NEW CODE
  const config = workspace.getConfiguration('coc-jls')
  const isEnable = config.get<boolean>('enable', true)
  if (!isEnable) {
    return
  }
  // END NEW CODE
  const serverOptions = {
    command: 'jedi-language-server', // run jls
  }
  const clientOptions = {
    documentSelector: ['python'], // run jls on py files
  }
  const client = new LanguageClient(
    'coc-jls', // the id
    'coc-jls', // the name of the language server
    serverOptions,
    clientOptions
  )
  context.subscriptions.push(services.registLanguageClient(client))
}
```

Now run `yarn` and voilà: users can now disable coc-jls without needing to uninstall the extension. Success!

### Deployment

To "deploy" this extension, one approach is to upload your project GitHub, add it to your Package or Plugin manager configuration, and install. If you're using [Vim-Plug](https://github.com/junegunn/vim-plug), put the following in your vimrc:

```vim
Plug 'your-username/coc-jls', {'do': 'yarn install --frozen-lockfile && yarn build'}
```

And run:

```vim
:PlugInstall
```

This will download your Git repository, install all necessary dependencies, build your project, and make sure it's automatically added to Vim's runtime path for coc can discover the extension.

You can also do all this manually if you know what you're doing.

Coc extensions can also be deployed to [npm](https://www.npmjs.com). This method is out of scope for this post, but you should be able to figure it out by referencing the [coc-jedi](https://github.com/pappasam/coc-jedi) codebase.

## Wrapping up

At this point, you should have a working coc extension that wraps an executable language server. You may be wondering how you can add more features, automatically download and manage the executable for your users, and make your coc extension the most user friendly interface since the [iPod click wheel](https://en.wikipedia.org/wiki/IPod_click_wheel). Worry not: these features are implemented in [coc-jedi](https://github.com/pappasam/coc-jedi). Please refer to that codebase and ask any further questions in the comments below. And don't feel obligated to restrict your wanderings to jedi-language-server: you can wrap **any** executable language server in a coc extension! Please use your powers for good.

![jedi programmer](https://www.kumulos.com/wp-content/uploads/2012/09/Computer-programming-jedi.jpg)

---
title: Gitignore: two tricks
date: 2018-12-02
category: software development
modified: 2018-12-02
tags: vcs, git
summary: Discover two techniques to ignore files from a Git-based version controlled project. The first technique enables Git to ignore every file in a directory other than the directory itself. The second technique enables a user to automatically ignore a file without adding it to a project's root gitignore.
description: Discover two techniques to ignore files with gitignore and git.
---

[TOC]

Most modern software developers are aware of [Git](https://git-scm.com/) and its accompanying [gitignore](https://git-scm.com/docs/gitignore) file. This post offers two lesser-known-yet-useful techniques to ignore files from a Git-based version controlled project. The first technique enables Git to ignore every file in a directory **but** the directory itself. The second technique enables a user to automatically ignore a file without adding it to a project's root gitignore.

Note: when discussing "[gitignore](https://git-scm.com/docs/gitignore)" and "[tern-project](http://ternjs.net/doc/manual.html#configuration)", I may sometimes add a "." before the filename. Whether I [do or do not](http://www.yodaquotes.net/try-not-do-or-do-not-there-is-no-try/), I'm talking about the same file (eg, ".gitignore" == "gitignore").

## Ignore directory contents, keep directory

It is often convenient to have a directory whose contents are not committed to version control. For example, this directory may contain large non-general data files (images, financial data, etc). Additionally, these could be small files with sensitive information specific to one person (passwords, ssh keys, etc). Either way, we do not want these files committed to our project's version control system. For the purposes of this conversation, we'll call this folder "instance" and place it at the root of our project.

```text
├── app
│   └── __init__.py
├── .gitignore          <-- Project gitignore
└── instance
    ├── big-file.jpg
    └── passwords.txt
```

A naive approach suggests that we add the instance folder to our project's gitignore:

```text
*.pyc
__pycache__/
# other ignored lines
instance/
```

Unfortunately, this proves problematic. What happens if our system relies on a file being in the instance folder at runtime? A user of our system would need to know to create the instance folder AND place a file there, forcing them to perform two manual steps.

A preferable solution: place a gitignore in the "instance" folder with special contents.

```text
├── app
│   └── __init__.py
├── .gitignore          <-- Project gitignore
└── instance
    ├── big-file.jpg
    ├── .gitignore      <-- Special gitignore
    └── passwords.txt
-----------------------------------
special .gitignore contents:
# Ignore all files in this directory
# EXCEPT for this .gitignore file
*
!.gitignore
```

I find myself using this trick so often that I've added the instance folder and its accompanying gitignore file into my project skeletons.

```bash
# ~/.bashrc (I actually use zsh + ~/.zshrc, but it's the same)
function make_instance() {
  mkdir instance
  cat > instance/.gitignore <<EOL
# Ignore all files in this directory
# EXCEPT for this .gitignore file
*
!.gitignore
EOL
}
```

Finally, you may note that this technique does commit one file (the [gitignore](https://git-scm.com/docs/gitignore)) to version control. IMHO, this is a small price to pay for elegance.

## Ignore my weird files (in secret)

My [development environment](https://github.com/pappasam/dotfiles) is highly customized. I'm an advanced user of [Neovim](https://neovim.io/charter/), [Tmux](https://www.ocf.berkeley.edu/~ckuehl/tmux/), [Zsh](http://zsh.sourceforge.net/Intro/intro_1.html#SEC1), and other [Unix-like](https://en.wikipedia.org/wiki/Unix-like) utilities, and have set up a cross-language, bespoke IDE with a configuration unto itself. Benefits include software development bliss. One downside: my environment may require files that I should not commit to another person's repository.

One example: when programming in Javascript, I rely on a [Tern](https://github.com/ternjs/tern) server for auto-completion in [Neovim](https://neovim.io/charter/). [Tern](https://github.com/ternjs/tern) is configurable with a [tern-project](http://ternjs.net/doc/manual.html#configuration) file which lets [Tern](https://github.com/ternjs/tern) know important things like the project's [ECMAScript](https://en.wikipedia.org/wiki/ECMAScript) version, which [runtime environment](http://voidcanvas.com/node-vs-browsers/) it's expecting, etc. These configurations differ by project, so it's often necessary for me to place a customized [tern-project](http://ternjs.net/doc/manual.html#configuration) file at the root of a Javascript project.

If I own a Javascript codebase and control its development, placing a [tern-project](http://ternjs.net/doc/manual.html#configuration) file at my project's root is a no-brainer. Not only can collaborators help me keep it up to date, but I can also influence more people to adopt [Tern](https://github.com/ternjs/tern)! Unfortunately, if I don't own the codebase I'm working on, things become a bit trickier. I want to benefit from [Tern](https://github.com/ternjs/tern) but I don't want my first contributions on a project to include my custom [development environment](https://github.com/pappasam/dotfiles) configuration. I'd simply add this file to the project's .gitignore file, but that would still be an me-specific contribution, so I'm left with two choices. Either I manually ignore [tern-project](http://ternjs.net/doc/manual.html#configuration) every time I "git add/commit", or I find a way to make Git do that work for me.

Luckily, Git has a built-in way for users to ignore their own weird files without needing to make any updates to a project's version-controlled files. This method is mentioned in [gitignore](https://git-scm.com/docs/gitignore)'s documentation, but not many people are aware it exists.

Using your favorite editor, go to the root of any [Git](https://git-scm.com/) repository, and open the text file ".git/info/exclude". It should look like this:

```bash
# Contents of PROJECT-ROOT/.git/info/exclude:
# git ls-files --others --exclude-from=.git/info/exclude
# Lines that start with '#' are comments.
# For a project mostly in C, the following would be a good set of
# exclude patterns (uncomment them if you want to use them):
# *.[oa]
# *~
```

Simply add your desired file patterns here and they will be ignored by you, and only you.

```bash
# Contents of PROJECT-ROOT/.git/info/exclude:
# git ls-files --others --exclude-from=.git/info/exclude
# Lines that start with '#' are comments.
# For a project mostly in C, the following would be a good set of
# exclude patterns (uncomment them if you want to use them):
# *.[oa]
# *~
.tern-project
```

Once you've done this, I recommend submitting one or two impressive pull requests. You should be invited as a repository [collaborator](https://help.github.com/articles/github-glossary/#collaborator) (or its equivalent) in no time. With credentials in hand, you can then suggest the group adopt your awesome [Tern](https://github.com/ternjs/tern)-based workflow (and your humble [tern-project](http://ternjs.net/doc/manual.html#configuration) file) into the project. At this point, you should remove the ".tern-project" line from .git/info/exclude.

## Conclusion

Ignoring directory contents while retaining directories is easy. Privately ignoring the files only you care about (for now) is also easy. Hopefully you learned something from this post and happy hacking!

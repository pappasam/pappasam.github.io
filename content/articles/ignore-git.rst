###############################
Gitignore-A-Palooza: Two Tricks
###############################

:date: 2018-12-02
:category: Software Development
:modified: 2018-12-02
:tags: version control, Git

Most modern software developers are aware of `Git https://git-scm.com/` and its
accompanying `.gitignore https://git-scm.com/docs/gitignore` file. This post
proposes two additional lesser-known techniques to ignore files from a
Git-based version controlled project. The first enables Git to ignore every
file in a directory **but** the directory itself. The second enables a user to
gitignore a file without adding it to a project's gitignore.

.. PELICAN_END_SUMMARY

1: Ignore a directory's contents, keep the directory
====================================================

It is often convenient to have a directory whose contents should not be
committed to version control. For example, this directory may contain large
non-general data files (images, financial data, etc). Additionally, these could
be small files with sensitive information specific to one person (passwords,
ssh keys, etc). Either way, we do not want these files committed to our
project's version control system. For the purposes of this conversation, we'll
call this folder "instance" and place it at the root of our project.

::

    ├── app
    │   └── __init__.py
    ├── .gitignore  <-- project's gitignore
    └── instance
        ├── big-file.jpg
        └── passwords.txt


A naive approach suggests that we add the instance folder to our project's
gitignore:

::

   *.pyc
   __pycache__/
   # other ignored lines
   instance/

Unfortunately, this proves problematic. What happens if our system relies on a
file being in the instance folder at runtime? A user of our system would need
to know to create the instance folder AND place a file there, forcing them to
perform two manual steps.

A preferable solution: place a gitignore in the "instance" folder with special
contents.

::

    ├── app
    │   └── __init__.py
    ├── .gitignore  <-- project's gitignore
    └── instance
        ├── big-file.jpg
        ├── .gitignore    <-- this file
        └── passwords.txt

    -----------------------------------

    .gitignore contents:
    # Ignore all files in this directory
    # EXCEPT for this .gitignore file
    *
    !.gitignore

I find myself using this trick so often that I've added the instance folder and
its accompanying gitignore file into my project skeletons.

2: Ignore my weird files in secret
==================================

My development environment is highly customized. I'm an expert user of Neovim
and have set up a cross-language, bespoke IDE with a configuration unto itself.
Benefits include software development bliss. One downside: my environment may
require files in a directory that I don't want to commit to another person's
repository.

One example: when programming in Javascript, I rely on Tern for
auto-completion. `Tern https://github.com/ternjs/tern` is configurable with a
".tern-project" file which lets Tern know important things like which version
of `ECMAScript https://en.wikipedia.org/wiki/ECMAScript` I'm using, which
runtime environment to expect, etc. These things differ by project so it's
often necessary to place a .tern-project file at the root of a project.

If I own a codebase and control its development, placing a .tern-project file
at my project root is a no-brainer. Not only can collaborators help me keep it
up to date, I can also influence more people to adopt `Tern
https://github.com/ternjs/tern`! Unfortunately, if I don't own the codebase I'm
working on, things become a bit trickier. I want to benefit from Tern but I
don't want my first contributions on a new project to include my custom IDE
configuration. I'd simply add this file to the project's .gitignore file, but
that would still be an IDE-specific contribution, so I'm left with two choices.
Either I manually ignore .tern-project every time I "git add" or "git commit",
or I find a way to make Git do that work for me.

Luckily, Git has a built-in way for users to ignore their own weird files
without needing to make any updates to a project's version-controlled files.
This method is documented in the gitignore `documentation
https://git-scm.com/docs/gitignore` although not may people are aware it
exists.

Using your favorite editor, go to the root of your project and open
".git/info/exclude". It should look like this:

.. code:: bash

    # git ls-files --others --exclude-from=.git/info/exclude
    # Lines that start with '#' are comments.
    # For a project mostly in C, the following would be a good set of
    # exclude patterns (uncomment them if you want to use them):
    # *.[oa]
    # *~

Simply add your desired file patterns here and they will be ignored
by you, and only you.

.. code:: bash

    # git ls-files --others --exclude-from=.git/info/exclude
    # Lines that start with '#' are comments.
    # For a project mostly in C, the following would be a good set of
    # exclude patterns (uncomment them if you want to use them):
    # *.[oa]
    # *~
    .tern-project

Once you've done this, I recommend getting one or two impressive pull requests
merged, becoming elevated to repository `collaborator
https://help.github.com/articles/github-glossary/#collaborator` or an
equivalent, and then proposing that the group accept your awesome tern-project
file into the project.

Conclusion
==========

Ignoring directories is easy. Privately ignoring the files only you care about
is also easy. Hopefully this post helped remove any confusion you may have felt
regarding gitignore, and happy hacking!

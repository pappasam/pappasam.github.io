###############################
Gitignore-A-Palooza: Two Tricks
###############################

:date: 2018-12-02
:category: Software Development
:modified: 2018-12-02
:tags: version control, Git

Most modern software developers are aware of Git_ and its accompanying
gitignore_ file. This post offers two lesser-known-yet-useful techniques to
ignore files from a Git-based version controlled project. The first technique
enables Git to ignore every file in a directory **but** the directory itself.
The second technique enables a user to automatically ignore a file without
adding it to a project's root gitignore.

.. PELICAN_END_SUMMARY

Note: when discussing "gitignore_" and "`tern-project`_", I may sometimes add a
"." before the filename. Whether I `do or do not`_, I'm talking about the same
file (eg, ".gitignore" == "gitignore").

1: Ignore directory contents, keep directory
============================================

It is often convenient to have a directory whose contents are not committed to
version control. For example, this directory may contain large non-general data
files (images, financial data, etc). Additionally, these could be small files
with sensitive information specific to one person (passwords, ssh keys, etc).
Either way, we do not want these files committed to our project's version
control system. For the purposes of this conversation, we'll call this folder
"instance" and place it at the root of our project.

::

    ├── app
    │   └── __init__.py
    ├── .gitignore          <-- Project gitignore
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

I find myself using this trick so often that I've added the instance folder and
its accompanying gitignore file into my project skeletons.

.. code:: bash

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

Finally, you may note that this technique does commit one file (the gitignore_)
to version control. IMHO, this is a small price to pay for elegance.

2: Ignore my weird files (in secret)
====================================

My `development environment`_ is highly customized. I'm an advanced user of
Neovim_, Tmux_, Zsh_, and other `Unix-like`_ utilities, and have set up a
cross-language, bespoke IDE with a configuration unto itself. Benefits include
software development bliss. One downside: my environment may require files that
I should not commit to another person's repository.

One example: when programming in Javascript, I rely on a Tern_ server for
auto-completion in Neovim_. Tern_ is configurable with a `tern-project`_ file
which lets Tern_ know important things like the project's ECMAScript_ version,
which `runtime environment`_ it's expecting, etc. These configurations differ
by project, so it's often necessary for me to place a customized
`tern-project`_ file at the root of a Javascript project.

If I own a Javascript codebase and control its development, placing a
`tern-project`_ file at my project's root is a no-brainer. Not only can
collaborators help me keep it up to date, but I can also influence more people
to adopt Tern_! Unfortunately, if I don't own the codebase I'm working on,
things become a bit trickier. I want to benefit from Tern_ but I don't want my
first contributions on a project to include my custom
`development environment`_ configuration. I'd simply add this file to the project's
.gitignore file, but that would still be an me-specific contribution, so I'm
left with two choices. Either I manually ignore `tern-project`_ every time I
"git add/commit", or I find a way to make Git do that work for me.

Luckily, Git has a built-in way for users to ignore their own weird files
without needing to make any updates to a project's version-controlled files.
This method is mentioned in gitignore_'s documentation, but not many people are
aware it exists.

Using your favorite editor, go to the root of any Git_ repository, and open the
text file ".git/info/exclude". It should look like this:

.. code:: bash

   # Contents of PROJECT-ROOT/.git/info/exclude:
   # git ls-files --others --exclude-from=.git/info/exclude
   # Lines that start with '#' are comments.
   # For a project mostly in C, the following would be a good set of
   # exclude patterns (uncomment them if you want to use them):
   # *.[oa]
   # *~

Simply add your desired file patterns here and they will be ignored by you, and
only you.

.. code:: bash

   # Contents of PROJECT-ROOT/.git/info/exclude:
   # git ls-files --others --exclude-from=.git/info/exclude
   # Lines that start with '#' are comments.
   # For a project mostly in C, the following would be a good set of
   # exclude patterns (uncomment them if you want to use them):
   # *.[oa]
   # *~
   .tern-project

Once you've done this, I recommend submitting one or two impressive pull
requests. You should be invited as a repository collaborator_ (or its
equivalent) in no time. With credentials in hand, you can then suggest the
group adopt your awesome Tern_-based workflow (and your humble `tern-project`_
file) into the project. At this point, you should remove the ".tern-project"
line from .git/info/exclude.

Conclusion
==========

Ignoring directory contents while retaining directories is easy. Privately
ignoring the files only you care about (for now) is also easy. Hopefully you
learned something from this post and happy hacking!

.. Begin: External hyperlinks

.. _`do or do not`: http://www.yodaquotes.net/try-not-do-or-do-not-there-is-no-try/
.. _ECMAScript: https://en.wikipedia.org/wiki/ECMAScript
.. _Git: https://git-scm.com/
.. _gitignore: https://git-scm.com/docs/gitignore
.. _Neovim: https://neovim.io/charter/
.. _Tern: https://github.com/ternjs/tern
.. _`tern-project`: http://ternjs.net/doc/manual.html#configuration
.. _Tmux: https://www.ocf.berkeley.edu/~ckuehl/tmux/
.. _Zsh: http://zsh.sourceforge.net/Intro/intro_1.html#SEC1
.. _`Unix-like`: https://en.wikipedia.org/wiki/Unix-like
.. _`development environment`: https://github.com/pappasam/dotfiles
.. _collaborator: https://help.github.com/articles/github-glossary/#collaborator
.. _`runtime environment`: http://voidcanvas.com/node-vs-browsers/

.. End: External hyperlinks

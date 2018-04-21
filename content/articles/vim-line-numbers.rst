################
Vim Line Numbers
################

:date: 2018-04-07
:category: Vim
:modified: 2018-04-07
:tags: Vim, Vim Plugins

TL;DR
=====

If you want your Vim line numbers to be relative and/or not relative at the
correct times, I recommend installing the `myusuf3/numbers.vim`_ plugin.

.. _`myusuf3/numbers.vim`: https://github.com/myusuf3/numbers.vim

The Problem
===========

When editing text in a Vim window, I use relative numbers to help me use
motions across text relative to my cursor. However, when I have multiple
windows open, relative numbers look pretty weird in windows that I am not
currently editing.  It would be nice for Vim to intelligently alternate between
relativenumber and norelativenumber based on my Vim cursor location. Base Vim
does not have this capability, so we have three options:

1. Accept a suboptimal workflow
2. Wrap our own solution in our .vimrc
3. Find a Plugin

I lived with option 1 for a while, but eventually grew too annoyed.  I then
tried researching plugins, but thought I understood the problem well-enough to
write my own solution. So I went straight to option 2 and tried wrapping my own
solution.

Wrapping my own solution
========================

The following code represents my original solution:

.. code-include:: vim-line-numbers/example.vim
    :lexer: vim
    :encoding: utf-8

The good
~~~~~~~~

The solution worked for most windows and tabs, most of the time.

The bad
~~~~~~~

The code is a bit involved and it takes a little time to explain to others.

1. It relies on window-local variables (w:line_number_state, etc).
   These exacerbate Vim's already-difficult state-management woes.
2. Several global functions are defined
3. There are some quirks I don't fully understand around the creation of
   variables during Vim startup (hence lines 50 and 51).

Despite these mild downsides, I was pretty proud that the solution mostly
worked. That is, until I wasn't.

The back-breaking straw
~~~~~~~~~~~~~~~~~~~~~~~

My custom solution did not work appropriately with some of my plugins. Namely,
it didn't play well with `majutsushi/tagbar`_, which I use frequently enough
for this feature-dearth to become royally annoying. Therefore, after learning
the ins-and-outs of window-specific variables and every Vim autocmd, I went
back to the Plugin ecosystem to see if I'd missed anything...

.. _`majutsushi/tagbar`: https://github.com/majutsushi/tagbar

The Game-Changing Plugin
========================

Turns out a wonderful developer already solved this problem for me.
Assuming you use `junegunn/vim-plug`_ to manage your plugins, place the
following code in your .vimrc

.. _`junegunn/vim-plug`: https://github.com/junegunn/vim-plug

.. code-block:: vim

    call plug#begin('~/.vim/plugged')
    " Relative Numbering
    Plug 'myusuf3/numbers.vim'
    " Put the rest of your plugins below...
    call plug#end()

    " Now, exclude the plugins you don't want numbers to deal with
    let g:numbers_exclude = ['startify', 'gundo', 'vimshell']

This will give you a great editing experience. See below for a screencast:

.. image:: {filename}/gif/numbers-vim.gif
    :alt: numbers.vim screencast
    :align: center

Conclusion
==========

Numbers.vim provides a usable line-numbering solution with minimal required
configuration. I regret nothing about my bespoke journey, but I'm glad that
Numbers.vim is my destination.

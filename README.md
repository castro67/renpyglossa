# Renpyglossa

*by Alejandro Castro García*

While doing some casual programming for Ren'Py, I ran into a few problems and ended using reusable solutions of my own, which may not be optimal, due to my inexperience with Ren'Py. Anyway, I am publishing them here, in case they are of interest to someone.

## File organization

This repository is organized into two directories:

* `libs`: the directory where modules of reusable code are kept, isolated except for some concise accompanying documentation.
* `samples`: the directory where some Ren'Py projects will be kept to illustrate how the reusable code can be used. The idea is that for each subdirectory of `libs`, there will be an equally named subdirectory of `samples`, illustrating the corresponding module of reusable code.

## Modules

As of this writing, I have three modules that I think are worth publishing::

* [Deque](libs/Deque): a limited but revertible alternative to `collections.deque`.
* [flexible_menu](libs/flexible_menu): a function to display menus, where choices can be enabled, disabled or hidden regardless of the value of `config.menu_include_disabled`.
* [prevep](libs/prevep): a way to load saved games from a previous episode in a game series.

## Samples

* [Deque](samples/Deque)
* [flexible_menu](samples/flexible_menu)
* [prevep](samples/prevep)

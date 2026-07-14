# Renpyglossa

*by Alejandro Castro García*

While doing some casual programming for Ren'Py, I ran into a few problems and ended using reusable solutions of my own, which may not be optimal, due to my inexperience with Ren'Py. Anyway, I am publishing them here, in case they are of interest to someone.

## File organization

This repository is organized into two directories:

* `libs`: the directory where modules of reusable code are kept, isolated except for some concise accompanying documentation.
* `samples`: the directory where some Ren'Py projects will be kept to illustrate how the reusable code can be used. The idea is that for each subdirectory of `libs`, there will be an equally named subdirectory of `samples`, illustrating the corresponding module of reusable code.

## Modules

As of this writing, I have three modules that I think are worth publishing. I want to revise them first, because it's been a while since I wrote them and I want to test them with the current Ren'Py version and add some documentation.

I have already revised one of them, so I am publishing it now:

* [Deque](libs/Deque): a limited but revertible alternative to `collections.deque`.
* [revep](libs/revep): a way to load saved games from a previous episode in a game series.

## Samples

* [Deque](samples/Deque)
* [revep](samples/revep)

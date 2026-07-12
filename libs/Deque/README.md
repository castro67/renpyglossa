# Deque documentation

The class `collections.deque` from the Python Standard Library is not revertible. For this reason, it does not work as expected with rollback and roll forward in Ren'Py games.

The class `Deque` here intends to provide a revertible alternative to `collections.deque`. It takes advantage of the fact that dictionaries and objects that do not inherit from non-revertible objects are revertible when created inside Ren'Py scripts.

To use the class, you only need to copy `Deque.rpy` to anywhere in your Ren'Py project where you would normally put Ren'Py scripts. The `game/libs` directory is a good choice, but it is not required as long as you take care that `Deque.rpy` is loaded before any code that uses it is executed.

The class `Deque` is not meant to be as complete as `collections.deque`, so not all methods are defined, but those that are defined are meant to use the same syntax and work the same way. The following methods and properties have been defined equivalent to those in `collections.deque`:

* `Deque([iterable [, maxlen]])`
* `append(item, /)`
* `appendleft(item, /)`
* `clear()`
* `pop()`
* `popleft()`
* `maxlen`

Additionally, just like objects of class `collections.deque`, an object `d` of class `Deque` supports the following constructs:

* `for elem in d:`
* `d[i]` (where `i` is an integer index)
* `len(d)`

Further extending `Deque` to better emulate `collections.deque` is not planned at the moment. It may happen if the need arises.

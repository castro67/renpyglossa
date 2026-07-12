# Copyright (c) Alejandro Castro García
# SPDX-License-Identifier: MIT

default log = Deque([], 5)

label start:

    scene image Solid("#222222")
    
    "This is an example of use of Deque, a revertible double-ended queue."

    "It works similarly to collections.deque from the Python Standard Library."
    
    "The Deque here is not as complete as collections.deque, but it's revertible."
    
    "This means it plays nicely with Ren'Py rollback and roll forward."
    
    "Let's see an example."
    

label test:
    call screen test_screen(log)
    
    $ print("RETURN:", _return)

    if (_return != "Finish"):
        $ log.append(_return)
        jump test
    
    "You have finished the test, but you should be able to roll back and then forward."
    "If I had used collections.deque from the Python Standard Library, then weird things would happen, like elements being added instead of removed when rolling back."
    "Only by using a custom Deque, we can trust that rolling back and forward will work as expected."
    menu:
        "Replay":
            $ log.clear()
            jump start
        "Exit":
            pass
    
    return


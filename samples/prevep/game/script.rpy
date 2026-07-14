# Copyright (c) Alejandro Castro García
# SPDX-License-Identifier: MIT

default gotprevious = False # True if we loaded from the first episode
default ep1 = {}    # Here we'll put the variables from the first episode


# prevep_init_vars and start_from_prevep are the two symbols that the game
# must define so that they are called from the prevep_slots screen when a
# previous episode save is loaded.

init python:
    def prevep_init_vars(prevdata):
        '''
        This is called immediately after loading a saved game from the
        previous episode, but before the game starts running.
        prevdata is a dictionary whose keys are variable identifiers from the
        previous episode.
        The default store is not usable yet, so we need to put the information
        we need at some place where we can retrieve it later.
        '''
        persistent.tmp_prevep = {} # I don't really need this to be persistent.
                                 # I just need that it can be accessed from
                                 # start_from_prevep below.
                                 # There should be a better way to do this, but
                                 # every other technique I tried caused some
                                 # kind of trouble.
       
# If we wished, we could import only those things from episode 1 that we need.
# But here I show how we would import everything from the store in episode 1.
        prefix = "store."                      
        for k in prevdata:
            if k.startswith(prefix):
                persistent.tmp_prevep[k[len(prefix):]] = prevdata[k]

label start_from_prevep:

    # After loading a saved game from the previous episode, the game starts
    # here, rather than at the start label. We move the loaded data to a more
    # convenient place.
    
    $ fill_ep1()
        
    $ gotprevious = True
    
    $ del persistent.tmp_prevep # Clean up, as persistent.tmp_prevep does not
                                # really need to be persistent and we don't
                                # want to pollute the persistent store
                                # (see prevep_init_vars() above).

    $ renpy.block_rollback()    # Deleting persistent.tmp_prevep may cause a
                                # crash if the user rolls back to the start.
                                # Blocking rollback here prevents this.

    # After we have made the proper initializations we jump to the
    # usual starting point.
    jump start

init python:
    def fill_ep1():
        # Instead of polluting the whole store with variables from episode 1,
        # we save them into their own dictionary ep1
        for k in persistent.tmp_prevep:
            store.ep1[k] = persistent.tmp_prevep[k]
    
    def last_dialogue_line():
        l = len(ep1["_history_list"])
        if l >= 1:
            return ep1["_history_list"][l - 1].what
        else:
            return None
        

label start:

    scene image Solid("#222222")
    
    if gotprevious:
        call saved_ending_start()
    else:
        call canonical_start()
    
    menu:
        "Main menu":
            pass
    return


label saved_ending_start():
    "You have started a new game by loading a saved game from \"The Question\", which we will treat as the first episode of a game series."
    "This is an example to illustrate the prevep module, whose goal is to load saves from previous episodes of the same game series."
    if not "book" in ep1:
        "Something went wrong with loading: the data loaded seems different from what the \"The Question\" is expected to save."
        "If loading had worked as expected, we would know whether, at the point of your save, you had chosen to define a visual novel as an interactive book or not."
        "We would not know anything else. We would not even know whether the game was finished or if you were walking towards the good ending or the bad ending."
    elif ep1["book"]:
        "At the point of your save, you had chosen to define a visual novel as an interactive book."
        "That's all we know. We don't know if you just made the choice or if you kept playing until reaching the good ending."
    else:
        "At the point of your save, you had not chosen to define a visual novel as an interactive book."
        "That's all we know. We don't know if you chose to define a visual novel as a videogame or if you weren't asked yet what a visual novel is. We don't even know if you finished the game or if you reached the good ending or the band ending."
    "That's because \"The question\" only defines one variable, named \"book\", indicating whether or not you defined a visual novel as an interactive book."
    "The prevep module that I use to load saves from a different game only reads variables. It does not directly know about logical lines or menu choices."
    "Ren'Py adds some additional variables that can help deduce where in the story the saved game is."
    if last_dialogue_line():
        $ say(None, 'For example, the last text in the history list in the game you loaded is: "' + last_dialogue_line() + '"')
    "But that's not very reliable, especially if the value of those variables depends on the preferred language of the player."
    "Because all I intended to do with this example was to show how to use prevep to load variables from another game, one variable is enough."
    "However, if you wish, you can easily modify \"The Question\" and this game to make them work better as two consecutive episodes of a game series."
    "In \"The Question\", you would have to define variables that indicate whether you have reached those checkpoints you deem important."
    "For example, use variables to indicate whether you decided to ask Sylvie now or later, whether you already defined what a visual novel is or whether you reached the bad or the good ending."
    "Every variable you add to the default store in your modified \"The Question\", will automatically appear in this game when you load from episode 1. For example, a variable named \"good_ending\" will appear as \"ep1\['good_ending'\]\" in this game."
    "Feel free to experiment."
    return

label canonical_start():
    "You have started a new game from scratch."
    "If this were the second episode of a real game, I could designate one of the endings of the first episode as canonical and start the second episode assuming that ending."
    "Alternatively, I could have made use of the {a=https://www.renpy.org/doc/html/persistent.html#multi-game-persistence}Multi-Game Persistence{/a} feature provided by Ren'Py and assume an ending actually played. If more than one ending was played, the one most recently played could be chosen, for example."
    "However, that is not the purpose of this example."
    "What I am trying to do here is use a saved game from the first episode as the starting point for the second episode."
    "For this example, I'll assume that the first episode of this game series is \"The Question\", the simple game to learn Ren'Py that you can find in your Ren'Py Launcher."
    "I assume version 7 of \"The Question\", included with Ren'Py 8.5.3."
    "So, to actually see what this example is about, go to your Ren'Py Launcher, launch \"The Question\" and save multiple games at different points of the story."
    "Then return to this game, go to the main menu and, instead of choosing \"Start\", choose \"Episode 1\"."
    return

    
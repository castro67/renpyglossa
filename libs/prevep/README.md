# prevep documentation

If you write a Ren'Py game series, you may want data from one episode to be available to the next episode. One documented way to achieve this is [Multi-Game Persistence](https://www.renpy.org/doc/html/persistent.html#multi-game-persistence).

However, there may be times when accessing the same persistent data in all episodes is not enough and what you really want is to be able to start a new game by loading a saved game from the previous episode. This is what the **prevep** module intends to do.

For the most part, **prevep** just adapts the same code that Ren'Py uses to load saved games so that files can be loaded from any directory.

## Usage

To use **prevep** in your game series you need to do the following:

1. Write each episode with its sequels in mind: write every information that may be of interest to sequels into the default store, so it's transferred to saved games.
2. Copy the `prevep.rpy` file into your sequel project `game` directory. I don't think it matters much where in `game` you place it. I most often use the `game/libs` directory, but this is not a requirement.
3. Somewhere in your main menu, there sould be a call to the `prevep_slots` screen, usually using `ShowMenu`. For example:

        textbutton previous_episode_title action ShowMenu("prevep_slots", previous_save_directory, prevep_screen_title)
    
    Here, `previous_save_directory` should be the value that `config.save_directory` has **in the previous episode**.
4. You need to implement the function `prevep_init_vars(prevdata)`. It will be called when loading a game from the previous episode before a new game is started.

    `prevdata` is simply a dictionary whose keys are variable names from your previous episode (prefixed with the name of the store) and whose values are the values of those variables at the time of the save.
    
    When your `prevep_init_vars()` function is invoked, the default store of your new game has not been created yet. Your implementation of `prevep_init_vars()` should write `prevdata` somewhere where it can be read from your new game once it starts. The **prevep** module does not define where to write this data. My particular choice is to temporarily use a field in the persistent object, but maybe there is a more adequate place.
5. You need to define a label called `start_from_prevep`. This label is where the game starts after loading a game from the previous episode. At this point, the default store of your new game has already been created, so you can move the data you saved in your `prevep_init_vars()` function to the default store or do whatever you want with that data.
6. Copy all custom classes from the previous episode into your new episode, unless you are sure that objects of those classes never get into saved games.

If you want to see a simple example, you can take a look at <https://github.com/castro67/renpyglossa/tree/main/samples/prevep>


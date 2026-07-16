# `flexible_menu()` documentation

`flexible_menu()` is a very small function to display menu choices, each of them described by a dictionary. It tries to let you do everything that can be done with the Ren'Py `menu` statement, while at the same time solve a particular limitation of this statement: its inability to indicate whether a particular choice should be hidden or shown as disabled when the expression in its if-clause evaluates to `False`.

## Usage

    flexible_menu(choice1, choice2, ...)

where each choice is a dictionary with the following format:

    {
        "text": text_of_the_choice,
        "value": value_of_the_choice,
        "if": true_if_choice_enabled, #(optional, True by default),
        "explain": appended_to_disabled_choice # (optional, empty by default),
        "exclude_disabled": true_if_should_hide_disabled  # (optional,
                                                             False by default)
    }

The return value is the value of the choice selected by the user.
    
`flexible_menu()` will simply use `renpy.display_menu()` to display the menu, based on these choice descriptions.

`flexible_menu()` assumes that a choice passed to `renpy.display_menu()` is shown as disabled if its value is `None`. You don't need to explicitly make `value=None`: `flexible_menu()` will convert the value to `None` before passing it to `renpy.display_menu()`if `choice["if"]==False`.

In reality, according to the documentation of `renpy.display_menu()`, a `None` value means that the choice is not an actual choice but a menu caption. This is not a problem as long as menu captions look like a disabled choice should look, which is true in the default appearance used by the Ren'Py Launcher for new projects. However, if you want to use actual menu captions that look distinct from disabled choices, then you probably need a different solution.

## Example

As an example, imagine this Ren'Py menu:

    menu:
        "Talk about the weather.":
            p "Hello. A nice sunny day, isn't it?"
            a "Yes, but I think it will rain tomorrow."
        "Buy sword (50 denarii)." if money >= 50 else disable():
                $ money -= 50
                $ swords += 1
                "You bought a sword."
        "Ask for help to rescue the princess." if princess_kidnapped else hide():
            p "Help! The princess has been kidnapped!"
        "Leave.":
            pass

This will, of course, crash with a syntax error, because the menu statement syntax does not expect constructs like `else disable()` and `else hide()` after the if-clause.

What I want to express is that, although disabled, I want the choice "Buy sword" to be shown, because I want players to be aware in advance of the possibility of buying a sword once they have enough money. However, the choice "Ask for help to rescue the princess" should be completely hidden until it is enabled, because showing it too early would be too big a spoiler.

The configuration variable `config.menu_include_disabled` doesn't help here, because it cannot be safely changed while the game is running, much less within the same menu.

With `flexible_menu()` we can achieve the desired effect with the following lines, regardless of the value of `config.menu_include_disabled`:

    init python:
        def my_menu():
            choice = flexible_menu(
                {
                    "text": "Talk about the weather.",
                    "value": "weather"
                },
                {
                    "text": "Buy sword (50 denarii).",
                    "value": "sword",
                    "if": money >= 50
                },
                {
                    "text": "Ask for help to rescue the princess.",
                    "value": "help",
                    "if": princess_kidnapped,
                    "exclude_disabled": True
                },
                {
                    "text": "Leave.",
                    "value": "leave"
                },
            )
            return choice
    $ choice = my_menu()
    if choice == "weather":
        p "Hello. A nice sunny day, isn't it?"
        a "Yes, but I think it will rain tomorrow."
    elif choice == "sword":
        $ money -= 50
        $ swords += 1
        "You bought a sword."
    elif choice == "help":
        p "Help! The princess has been kidnapped!"

This is not as nice and simple as the menu statement, but it's reasonably legible and does the job: it shows the choice "Buy sword" as disabled if you don't have enough money and it completely hides the choice "Ask for help to rescue the princess" if she does not need to be rescued.

If you want to see an extended version of this example ready to be built, you can take a look at <https://github.com/castro67/renpyglossa/tree/main/samples/flexible_menu>


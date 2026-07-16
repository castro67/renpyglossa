# Copyright (c) Alejandro Castro García
# SPDX-License-Identifier: MIT

define p = Character("Publius", who_color="#00ffff")
define pt = Character("Publius", who_color="#00ffff", what_color="#777777", what_italic=True)
define a = Character("Armourer", who_color="#ff7777")
define pr = Character("Princess", who_color="#ff77ff")

default money = 10
default swords = 0
default princess_kidnapped = False
default talk1 = [False, False, False]
default flexible_shown = False


label start:

    scene image Solid("#222222")
    
    pt "I think I should buy a sword."
    pt "Hmm... This guy sells swords..."
    

label talk_armourer1:
    menu:
        "Choose every option in turn. You can continue once you have tried all the options."

        "Talk about the weather.":
            call process_choice("weather")
            $ talk1[0] = True
        "Buy sword.":
            call process_choice("sword")
            $ talk1[1] = True
        "Ask for help to rescue the princess.":
            if princess_kidnapped:
                p "Help! The princess has been kidnapped!"
            else:
                "The princess was not kidnapped yet."
            $ talk1[2] = True
    if not talk1_done():
        jump talk_armourer1


    "As you can see, there is a problem with the previous menu."
    "There are two options that do nothing. It would be better if they were disabled."
    "We can conditionally disable an option by adding an if-clause to it. Let's try..."
    
label talk_armourer2:
    menu:
        "Talk about the weather.":
            p "Hello. A nice sunny day, isn't it?"
            a "Yes, but I think it will rain tomorrow."
        "Buy sword (50 denarii)." if money >= 50:
                $ money -= 50
                $ swords += 1
                "You bought a sword."
        "Ask for help to rescue the princess." if princess_kidnapped:
            p "Help! The princess has been kidnapped!"
        "Leave.":
            pass
    
    "Now only the options that actually work are shown."
    "But that creates a new problem: it may not be immediately obvious to the player why Publius can't buy a sword."
    "That's why Ren'Py has a configuration variable that allows to show disabled menu options, but in a dimmed, non-clickable state."
    "This configuration variable is called menu_include_disabled. If its value is True, then disabled menu options are still not selectable, but they are shown."
    "Because menu_include_disabled is not set for this game and it's not advisable to change configuration variables at run time, I cannot add a real example, but I can emulate the effect through programming."
    call talk_armourer3()
    
    "Now the player gets a hint that, if Publius wants to buy a sword, he needs to earn money."
    "But there is still one problem."
    "We wanted to know why Publius couldn't buy a sword..."
    "... but we didn't want to know that the princess will need to be rescued at some point."
    "That's a major spoiler."
    "So we have a choice that we want to be shown when disabled and another choice that we want hidden when disabled."
    "The configuration variable menu_include_disabled is not enough for that, but we can mix both kinds of disabled items with the help of the renpy.display_menu() function."
    "My flexible_menu() function just tries to make it easier to describe how we want to display the disabled choices before calling renpy.display_menu()."

label visit_armourer:
    call talk_armourer4()
    "Go to other places to change the game state and then visit the armourer again."

label wheretogo:
    menu:
        "Where should I go now?"
        
        "Visit the armourer.":
            jump visit_armourer
        "Visit the princess.":
            if princess_kidnapped:
                $ princess_kidnapped = False
                pr "Hi."
                p "Oh, I thought you had been kidnapped."
                pr "I was, but I've been rescued."
            else:
                $ princess_kidnapped = True
                pt "Oh no! Someone has kidnapped the princess."
        "Earn money." if money < 50:
            $ money = 50
        "Squander your money." if money >= 50:
            $ money = 10
        "The End.":
            jump ending
    jump wheretogo 

label ending:
    "That's all. Check the source code to see if it fits your programming needs."
    menu:
        "Replay":
            $ money = 10
            $ swords = 0
            $ princess_kidnapped = False
            $ talk1 = [False, False, False]
            $ flexible_shown = False
            jump start
        "Main menu":
            pass
    return

label talk_armourer3():
    $ narrator("This is how our menu would look if we had used menu_include_disabled=True", interact=False)
    call process_choice(menu_include_all_disabled())
    return

label talk_armourer4():
    if flexible_shown:
        $ narrator("Same menu as before, but it will look different depending on the game state.", interact=False)
    else:
        $ flexible_shown = True
        $ narrator("Now we don't see the rescue spoiler. It's still there in the menu description passed to flexible_menu(), but it's only shown if enabled.", interact=False)
    call process_choice(menu_exclude_spoilers())
    return

label process_choice(choice):
    if choice == "weather":
        p "Hello. A nice sunny day, isn't it?"
        a "Yes, but I think it will rain tomorrow."
    elif choice == "sword":
        if money < 50:
            "You don't have 50 denarii."
        else:
            $ money -= 50
            $ swords += 1
            "You bought a sword."
    elif choice == "help":
        if princess_kidnapped:
            p "Help! The princess has been kidnapped!"
        else:
            "The princess was not kidnapped yet."
    return

init python:

    def talk1_done():
        return (talk1[0] and talk1[1] and talk1[2])
    
    def menu_include_all_disabled():
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
                "if": princess_kidnapped
            },
            {
                "text": "Leave.",
                "value": "leave"
            },
        )
        return choice

    def menu_exclude_spoilers():
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

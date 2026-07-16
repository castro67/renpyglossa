# Copyright (c) Alejandro Castro García
# SPDX-License-Identifier: MIT

init python:
    '''
    flexible_menu() accepts an indeterminate number of parameters. Each
    parameter represents a choice, expressed as a dictionary with the following
    form:
    
    {
        "text": text_of_the_choice,
        "value": value_of_the_choice,
        "if": true_if_choice_enabled, #(optional, True by default),
        "explain": appended_to_disabled_choice # (optional, empty by default),
        "exclude_disabled": true_if_should_hide_disabled  # (optional,
                                                             False by default)
    }
    '''
    def flexible_menu(*choices):
        items = []
        for choice in choices:
            text = __(choice["text"]);
            value = choice["value"];
            if "if" in choice and not choice["if"]:
                if ("exclude_disabled" in choice and
                            choice["exclude_disabled"]):
                    continue
                value = None
                if "explain" in choice and choice["explain"] != "":
                    text += " " + __(choice["explain"])
            items.append((text, value))
        return renpy.display_menu(items)


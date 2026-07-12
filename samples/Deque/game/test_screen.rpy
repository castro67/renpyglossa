# Copyright (c) Alejandro Castro García
# SPDX-License-Identifier: MIT

screen test_screen(log):
    roll_forward True


    vbox:
        xalign 0.1 ypos 0.15
        spacing 3
        frame:
            text "log"
        frame:
            xminimum 62
            yminimum 50
            vbox:
                for t in log:
                    text t xoffset 12

    hbox:
        xalign 0.1
        ypos 0.7
        text "We have a Deque called log, initially empty, with a limit of 5 elements." xmaximum 500

    hbox:
        xalign 0.9
        ypos 0.7
        text "Every time you press a digit, it will be added to log. If log grows beyond 5 elements, the oldest ones will be removed." xmaximum 500

    vbox:
        xalign 0.9 ypos 0.15
        spacing 2
        hbox:
            spacing 2
            frame:
                textbutton "7":
                    action Return("7")
            frame:
                textbutton "8":
                    action Return("8")
            frame:
                textbutton "9":
                    action Return("9")
        hbox:
            spacing 2
            frame:
                textbutton "4":
                    action Return("4")
            frame:
                textbutton "5":
                    action Return("5")
            frame:
                textbutton "6":
                    action Return("6")
        hbox:
            spacing 2
            frame:
                textbutton "1":
                    action Return("1")
            frame:
                textbutton "2":
                    action Return("2")
            frame:
                textbutton "3":
                    action Return("3")
        hbox:
            spacing 2
            frame:
                textbutton "0":
                    action Return("0")

    if len(log) >= 5:
        frame:
            xalign 0.5 yalign 0.2
            textbutton "Finish":
                action Return("Finish")

        hbox:
            xalign 0.5 yalign 0.4
            text "Now log is full. You can keep adding digits to see how the oldest elements are removed. Press \"Finish\" when you get bored." xmaximum 500


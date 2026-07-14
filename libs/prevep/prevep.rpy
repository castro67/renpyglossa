# Copyright (c) Alejandro Castro García
# SPDX-License-Identifier: MIT

# A module to load saved games from a previous episode.

# A lot of code in this module has been adapted from Ren'Py software,
# in particular from the following files from <https://github.com/renpy>:
# - gui/game/screens.rpy
# - renpy/loadsave.py
# - renpy/savelocation.py
# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
# License: <https://www.renpy.org/doc/html/license.html>

screen prevep_slots(prevepdir, title):
# Copied from file_slots in screens.rpy with some modifications

# prevepdir should be equal to config.save_directory from the previous episode

# title works similary to title argument for file_slots

    tag menu
    default emptyslot = Null(width=config.thumbnail_width, height=config.thumbnail_height)
    use game_menu(title):
        fixed:

            $ currentpage = prevep_currentpage(prevepdir)   # Our current page
                                            # is independent from the current
                                            # page used by file_slots

            ## The page name, which I don't bother to make editable
            $ strpage = prevep_strpage(currentpage)

            $ page_name = prevep_pagename(currentpage)
            text page_name:
                style "page_label_text"
                xalign 0.5

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing
                

                for i in range(gui.file_slot_cols * gui.file_slot_rows):
                    $ slot = i + 1
                    $ ss = prevep_screenshot(prevepdir, slot, strpage)
                    $ mtime = prevep_mtime(prevepdir, slot, strpage, _("{#file_time}%A, %B %d %Y, %H:%M"))
                    $ slotname = prevep_slotname(prevepdir, slot, strpage)

                    button:
                        if ss is not None:
                            if main_menu:
                                action Function(prevep_start, prevepdir, slot, strpage)
                            else:
#                                action Confirm(gui.LOADING, yes=Function(prevep_start, prevepdir, slot, strpage))
                                pass    # Trying to load from previous episode
                                        # does not work well in the middle of
                                        # a game, because loading from previous
                                        # episode is more similar to start a
                                        # new game than to load a saved game
                        has vbox
                        if ss is not None:
                            add ss xalign 0.5 xsize config.thumbnail_width ysize config.thumbnail_height # Explicit size to fit in the slot, in case the previous episode has a different size
                        else:
                            add emptyslot xalign 0.5
                        if mtime is None:
                            text _("empty slot"):
                                style "slot_time_text"
                        else:
                            text mtime:
                                style "slot_time_text"

                        if slotname is not None:
                            text slotname:
                                style "slot_name_text"
           ## Buttons to access other pages.
            vbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                hbox:
                    xalign 0.5

                    spacing gui.page_spacing

                    textbutton _("<") action Function(prevep_prevpage, prevepdir)
                    key "save_page_prev" action Function(prevep_prevpage, prevepdir)

                    if config.has_autosave:
                        textbutton _("{#auto_page}A") action Function(prevep_gotopage, prevepdir, -1)

                    if config.has_quicksave:
                        textbutton _("{#quick_page}Q") action Function(prevep_gotopage, prevepdir, 0)

                    ## range(1, 10) gives the numbers from 1 to 9.
                    for page in range(1, 10):
                        textbutton "[page]" action Function(prevep_gotopage, prevepdir, page)

                    textbutton _(">") action Function(prevep_nextpage, prevepdir)
                    key "save_page_next" action Function(prevep_nextpage, prevepdir)

init python:

    def prevep_path(prevepdir, slot, page):
        from pathlib import Path
        prevep_savedir = str((Path(config.savedir).parent / prevepdir).absolute())
        return prevep_savedir + "/" + page + "-" + str(slot) + "-LT1.save"

    def prevep_screenshot(prevepdir, slot, page):
        # This is adapted from Ren'Py code: screenshot in savelocation.py.
        # I didn't call that directly because I don't know if there is a way
        # to make it use a slot from a different save location.
        import zipfile
        import os
        path = prevep_path(prevepdir, slot, page)
        try:
            mtime = os.path.getmtime(path)
            with zipfile.ZipFile(path, "r") as zf:
                try:
                    png = False
                    zf.getinfo("screenshot.tga")
                except Exception:
                    png = True
                    zf.getinfo("screenshot.png")
            if png:
                screenshot = renpy.display.im.ZipFileImage(path, "screenshot.png", mtime)
            else:
                screenshot = renpy.display.im.ZipFileImage(path, "screenshot.tga", mtime)
        except Exception as e:
            return None

        return screenshot

    def prevep_mtime(prevepdir, slot, page, format):
        # This is adapted from Ren'Py code: mtime in savelocation.py.
        import os
        import time
        path = prevep_path(prevepdir, slot, page)
        try:
            mtime = os.path.getmtime(path)
        except Exception:
            return None
        format = renpy.translation.translate_string(format)
        mtimef = _strftime(format, time.localtime(mtime))
        return mtimef

    def prevep_slotname(prevepdir, slot, page):
        # This is adapted from Ren'Py code: json in savelocation.py.
        import zipfile
        import json
        from renpy.compat.pickle import loads
        path = prevep_path(prevepdir, slot, page)
        try:
            with zipfile.ZipFile(path, "r") as zf:
                try:
                    data = zf.read("json")
                    data = json.loads(data)
                    return data["_save_name"]
                except Exception:
                    pass
                try:
                    name = zf.read("extra_info").decode("utf-8")
                except Exception:
                    return None
        except Exception:
            return None
        return name

    def prevep_currentpage(prevepdir):
        if persistent.prevep_currentpage is None:
            persistent.prevep_currentpage = {}
        if not prevepdir in persistent.prevep_currentpage:
            persistent.prevep_currentpage[prevepdir] = 1
        return persistent.prevep_currentpage[prevepdir]
        
    def prevep_setcurrentpage(prevepdir, page):
        if (page < -1):
            page = -1
        if persistent.prevep_currentpage is None:
            persistent.prevep_currentpage = {}
        persistent.prevep_currentpage[prevepdir] = page
     
    def prevep_nextpage(prevepdir):
        prevep_setcurrentpage(prevepdir, prevep_currentpage(prevepdir) + 1)

    def prevep_prevpage(prevepdir):
        prevep_setcurrentpage(prevepdir, prevep_currentpage(prevepdir) - 1)

    def prevep_gotopage(prevepdir, page):
        prevep_setcurrentpage(prevepdir, page)

    def prevep_strpage(page):
        if page == -1:
            return "auto"
        elif page == 0:
            return "quick"
        else:
            return str(page)

    def prevep_pagename(page):
        if page == -1:
            return "Automatic saves"
        elif page == 0:
            return "Quick saves"
        else:
            return "Page " + str(page)

    def prevep_load(prevepdir, slot, page):
        # This is adapted from Ren'Py code: load in loadsave.py and load
        # in savelocation.py. I didn't call those directly because I don't
        # know if there is a way to make them use a slot from a different
        # save location.
        import zipfile
        from renpy.compat.pickle import loads
        path = prevep_path(prevepdir, slot, page)
        try:
            with zipfile.ZipFile(path, "r") as zf:
                log_data = zf.read("log")
    
                try:
                    signature = zf.read("signatures").decode("utf-8")
                except:
                    signature = ""
            if not renpy.savetoken.check_load(log_data, signature):
                return
            roots, log = loads(log_data)
        except FileNotFoundError:
            return {"error": "filenotfound"}
#         for k in roots:
#             print(k, roots[k])
        '''
        We don't return rollback information (log), because rollback from the
        previous episode is meaningless to the new one and, anyway, loading
        from a previous episode always should start a new game.
        '''
        return roots

    def prevep_start(prevepdir, slot,page):
        tmp = prevep_load(prevepdir, slot, page)   # In tmp we have the data
        prevep_init_vars(tmp)   # prevep_init_vars will have to be implemented
                                # by the particular game

        renpy.run(Start("start_from_prevep"))   # start_from_prevep has to be
                                                # implemented by the particular
                                                # game
    

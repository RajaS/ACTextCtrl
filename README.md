Auto Complete TextCtrl for WxPython
-----------------------------------

I am often using comboboxes on forms, but want something that allows
more rapid data entry. This textctrl is designed to allow the user
to quickly select from a list of choices by dynamically presenting
matches in a dropdown below the textctrl. Similar implementations exist,
notably http://wiki.wxpython.org/TextCtrlAutoComplete, from which a lot
a lot of code is borrowed, but this is too complex for my needs.

The widget is designed to present a textctrl into which the user starts
typing. Matches (configurable to matches at beginning or matches anywhere)
to the typed text will appear in a dropdown box. Up and down arrow keys can
be used to navigate among the matches. Enter key will populate the textctrl
with the selected match. Tab key will expand the entered text to the current
match. When text is entered that does not have a match, an option exists to
allow the user to add this text to the choices available.

Note that this is still in the early changes. As of now, this has only been
tested on Linux with Python 2.6 and 2.7 and WxPython 2.8.

![](https://github.com/RajaS/ACTextCtrl/raw/master/screenshot.png)

# Written to satisfy my need for a text entry widget with autocomplete.
# Heavily borrowed ideas from http://wiki.wxpython.org/TextCtrlAutoComplete
# Raja Selvaraj <rajajs@gmail.com>

import wx



class ACTextControl(wx.TextCtrl):
    """
    A Textcontrol that accepts a list of choices at the beginning.
    Choices are presented to the user based on string being entered.
    If a string outside the choices list is entered, option may
    be given for user to add it to list of choices.
    """
    def __init__(self, parent, choices=[], add_option=False):
        wx.TextCtrl.__init__(self, parent, style=wx.TE_PROCESS_ENTER)

        self.all_choices = choices
        self.add_option = add_option

        self.popup = ACPopup(self)

        self._set_bindings()
        

    def _set_bindings(self):
        """
        One place to setup all the bindings
        """
        # text entry triggers update of the popup window
        self.Bind(wx.EVT_TEXT, self.on_text, self)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down, self)


    def on_text(self, event):
        """
        On text entry in the textctrl,
        Pop up the popup,
        or update choices if its already visible
        """
        if not self.popup.IsShown():
            self.position_popup()

        txt = event.GetString()
        select_choices = [ch for ch in self.all_choices if txt in ch]
            
        self.popup._set_choices(select_choices)

        if not self.popup.IsShown():
            self.popup.Show()
        

    def position_popup(self):
        """Calculate position for popup and
        display it"""
        left_x, upper_y = self.GetScreenPositionTuple()
        _, height = self.GetSizeTuple()
        self.popup.SetPosition((left_x, upper_y + height))
        #self.popup._set_choices(self.all_choices)
        #self.popup.Show()


    def on_key_down(self, event):
        """Handle key presses.
        Special keys are handled appropriately.
        For other keys, the event is skipped and allowed
        to be caught by ontext event"""
        skip = True
        visible = self.popup.IsShown() 

        # Escape key closes the popup if it is visible
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            if visible:
                self.popup.Show(False)
        
        if skip:
            event.Skip()

            

class ACPopup(wx.PopupWindow):
    """
    The popup that displays the autocomplete choices.
    """
    def __init__(self, parent):
        wx.PopupWindow.__init__(self, parent)
        self.choicebox = wx.ListBox(self, -1, choices=[])
        self.SetSize((100, 100))
        self.displayed_choices = []

    def _set_choices(self, choices):
        """
        Clear existing choices and use the supplied choices
        Choices is a list of strings.
        """
        # if there is no change, do not update
        if sorted(choices) == sorted(self.displayed_choices):
            pass

        self.choicebox.Set(choices)
        self.displayed_choices = choices

        

def test():
    app = wx.PySimpleApp()
    frm = wx.Frame(None, -1, "Test", style=wx.DEFAULT_FRAME_STYLE)
    panel = wx.Panel(frm)
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    
    choices = ['cat', 'dog']
    
    ctrl = ACTextControl(panel, choices=choices)
    sizer.Add(ctrl, 1, wx.ADJUST_MINSIZE, 10)
    
    panel.SetAutoLayout(True)
    panel.SetSizer(sizer)
    sizer.Fit(panel)
    sizer.SetSizeHints(panel)
    panel.Layout()
    app.SetTopWindow(frm)
    frm.SetSize((400, 200))
    frm.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()

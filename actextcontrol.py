
# Written to satisfy my need for a text entry widget with autocomplete.
# Heavily borrowed ideas from http://wiki.wxpython.org/TextCtrlAutoComplete
# Raja Selvaraj <rajajs@gmail.com>


##  CAUTION: WORK IN PROGRESS ##

import wx



class ACTextControl(wx.TextCtrl):
    """
    A Textcontrol that accepts a list of choices at the beginning.
    Choices are presented to the user based on string being entered.
    If a string outside the choices list is entered, option may
    be given for user to add it to list of choices.
    match_at_start - Should only choices beginning with text be shown ?
    add_option - Should user be able to add new choices
    """
    def __init__(self, parent, choices=[], match_at_start = False,
                 add_option=False):
        wx.TextCtrl.__init__(self, parent, style=wx.TE_PROCESS_ENTER)

        self.all_choices = choices
        self.match_at_start = match_at_start
        self.add_option = add_option
        self.max_choices = 5   # maximum no. of choices to show
        
        self.popup = ACPopup(self)

        self._set_bindings()
        

    def _set_bindings(self):
        """
        One place to setup all the bindings
        """
        # text entry triggers update of the popup window
        self.Bind(wx.EVT_TEXT, self.on_text, self)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down, self)

        # loss of focus should hide the popup
        self.Bind(wx.EVT_KILL_FOCUS, self.on_focus_loss)
        
        
    def on_text(self, event):
        """
        On text entry in the textctrl,
        Pop up the popup,
        or update choices if its already visible
        """
        txt = event.GetString()

        # if txt is empty (after backspace), hide popup
        if not txt:
            if self.popup.IsShown:
                self.popup.Show(False)
                event.Skip()
                return

        # Bring up the popup if it is not there
        if not self.popup.IsShown():
            self.position_popup()

        # Select choices to display
        if self.match_at_start:
            select_choices = [ch for ch in self.all_choices
                              if ch.startswith(txt)]
        else:
            select_choices = [ch for ch in self.all_choices if txt in ch]

        # TODO:
        # order the choices (alphabetical sort / frecency?)
            
        if len(select_choices) == 0:
            if not self.add_option:
                if self.popup.IsShown():
                    self.popup.Show(False)

            else:
                display = ['Add ' + txt]
                self.popup._set_choices(display, 'Add')
                self.resize_popup(display, txt)
                if not self.popup.IsShown():
                    self.popup.Show()
                
        else:
            # set up the popup and bring it on
            self.popup._set_choices(select_choices, txt)
            self.resize_popup(select_choices, txt)
        
            if not self.popup.IsShown():
                self.popup.Show()
        

    def on_focus_loss(self, event):
        """Close the popup when focus is lost"""
        if self.popup.IsShown():
            self.popup.Show(False)

                
    def position_popup(self):
        """Calculate position for popup and
        display it"""
        left_x, upper_y = self.GetScreenPositionTuple()
        _, height = self.GetSizeTuple()
        self.popup.SetPosition((left_x, upper_y + height))


    def resize_popup(self, choices, entered_txt):
        """Calculate the size for the popup to
        accomodate the selected choices"""
        # Handle empty list (no matching choices)
        if len(choices) == 0:
            choice_count = 3.5 # one line
            longest = len(entered_txt) + 4 + 4 #4 for 'Add '

        else:
            # additional 3 lines needed to show all choices without scrollbar        
            choice_count = min(self.max_choices, len(choices)) + 2.5
            longest = max([len(choice) for choice in choices]) + 4

        
        charheight = self.popup.choicebox.GetCharHeight()
        charwidth = self.popup.choicebox.GetCharWidth()

        self.popupsize = wx.Size( charwidth*longest, charheight*choice_count )

        self.popup.choicebox.SetSize(self.popupsize)
        self.popup.SetClientSize(self.popupsize)
        

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
        self.choicebox = wx.SimpleHtmlListBox(self, -1, choices=[])
        self.SetSize((100, 100))
        self.displayed_choices = []

    def _set_choices(self, choices, txt):
        """
        Clear existing choices and use the supplied choices
        Choices is a list of strings.
        """
        # if there is no change, do not update
        if sorted(choices) == sorted(self.displayed_choices):
            pass

        # Remove the current choices
        self.choicebox.Clear()
        
        #self.choicebox.Append(['te<b>st</b>', 'te<b>st</b>'])
        for ch in choices:
            self.choicebox.Append(self.htmlformat(ch, txt))

        self.displayed_choices = choices


    def htmlformat(self, text, substring):
        """
        For displaying in the popup, format the text
        to highlight the substring in html
        """
        # empty substring
        if len(substring) == 0:
            return text

        else:
            return text.replace(substring, '<b>' + substring + '</b>')
        

def test():
    app = wx.PySimpleApp()
    frm = wx.Frame(None, -1, "Test", style=wx.DEFAULT_FRAME_STYLE)
    panel = wx.Panel(frm)
    
    choices = ['cat', 'dog', 'rat', 'pig', 'tiger', 'elephant', 'ant',
               'horse']

    label1 = wx.StaticText(panel, -1, 'Matches anywhere in string')
    label2 = wx.StaticText(panel, -1, 'Matches only at beginning')
    label3 = wx.StaticText(panel, -1, 'Allows new choices to be added')
               
    ctrl1 = ACTextControl(panel, choices=choices, add_option=False)
    ctrl2 = ACTextControl(panel, choices=choices, match_at_start=True, add_option=False)
    ctrl3 = ACTextControl(panel, choices=choices, add_option=True)

    sizer = wx.BoxSizer(wx.HORIZONTAL)
    
    fgsizer = wx.FlexGridSizer(rows=3, cols=2, vgap=20, hgap=5)
    fgsizer.AddMany([label1, ctrl1,
                     label2, ctrl2,
                     label3, ctrl3])
    
    panel.SetAutoLayout(True)
    panel.SetSizer(fgsizer)
    fgsizer.Fit(panel)
    #sizer.SetSizeHints(panel)

    sizer.Add(panel, 1, wx.ALL, 20)
    frm.SetSizer(sizer)
    
    panel.Layout()
    app.SetTopWindow(frm)
    frm.SetSize((400, 200))
    frm.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()

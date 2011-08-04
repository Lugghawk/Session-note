'''
Created on 2011-08-04

@author: dl250074

http://matgnt.wordpress.com/2009/11/08/eclipse-pydev-and-gtk-with-code-completion/
'''

import sys

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass

try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)
    
class UI:
    

    def on_mainWindow_destroy (self,widget,data=None):
        gtk.main_quit()
        
    def row_selected(self,widget,data=None):
        self.noteList.clear()
        
    def show_selectednote(self,widget,data=None):
        print self.selectedNote.get_selected()
        
    
    
    def __init__(self):
        #Set the gladefile
        filename = "main.glade"
        builder = gtk.Builder()
        builder.add_from_file(filename)
        
        self.window = builder.get_object("window1")
        testList = [['Daves Note','Dave Lugg'],['Daves Note 2','Dave Lugg']]
        self.noteList = builder.get_object("noteList")
        for nodes in testList:
            self.noteList.append(nodes)
            
        builder.connect_signals(self)
        
        self.selectedNote = builder.get_object("noteListView").get_selection()
        
        
        
    

if __name__ == '__main__':
    app = UI()
    gtk.main()
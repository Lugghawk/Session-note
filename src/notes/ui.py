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
    
    def get_note_name(self, treeView, path):
        #Pretty dirty way to return the value of the first column in the selected row
        #This function takes a treeView object, and path object given to this function by a gtk event handler.
        #It will return the value of the first (0) column, in the first element in the selected rows tuple.
        #Selected_rows returns a tuple of the index of all rows selected. If one is selected, the 0th element is its index
        return treeView.get_selection().get_selected_rows()[0][path[0]][0]
    
    def show_highlighted_note(self, treeview, path, view_column, userData=None):
        print self.get_note_name(treeview,path)
    
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
        
        
        
              
        
    

if __name__ == '__main__':
    app = UI()
    gtk.main()
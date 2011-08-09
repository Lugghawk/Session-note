'''
Created on 2011-08-04

@author: dl250074

http://matgnt.wordpress.com/2009/11/08/eclipse-pydev-and-gtk-with-code-completion/
'''

import sys,configuration, os

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
        noteBuffer = self.builder.get_object("noteBuffer")
#        print self.list_object_names()
        note = open (self.configFile.repoLocation()+"\\" + str(self.get_note_name(treeview,path)) )
        
        noteBuffer.set_text(note.read())
    
    def list_object_names(self):
        objects = self.builder.get_objects()
        for stuff in objects:
            print stuff
    
    def __init__(self, config):
        #Set the gladefile
        filename = "main.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(filename)
        
        self.configFile = config
        self.listNotes = []
        self.createNoteList(self.configFile.repoLocation())
        
        self.window = self.builder.get_object("window1")
        
        self.noteList = self.builder.get_object("noteList")
        
        for nodes in self.listNotes:
            self.noteList.append(nodes)
            pass
            
        self.builder.connect_signals(self)
    
    def createNoteList(self,repoLocation):
        '''
        This method will create a list within a list of [Note Filename],[Author] pairs of each of the notes within the repository.
        '''
        dir = os.listdir(repoLocation)
        for fname in dir:
            if fname[-3:] == self.configFile.session_note_extension:
                self.listNotes.append([fname, self.getNoteAuthor(fname)])
            
    def getNoteAuthor(self, noteName):
        '''
        Currently this will spread out the initials used in the session note filename.
        This should be extended to take the template into account 
        '''
        authInitials = noteName.split("-")[1]
        newInitials = ''
        authInitials = authInitials.upper()
        for chars in authInitials:
            newInitials += chars +"."
            
        return newInitials
             
        
        
                  
        
    

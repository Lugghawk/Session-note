'''
Created on 2011-08-04

@author: dl250074

http://matgnt.wordpress.com/2009/11/08/eclipse-pydev-and-gtk-with-code-completion/
'''

import sys,configuration, os, mypygit

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
        #This will copy the text in the session note into noteBuffer and display it.
        noteBuffer = self.builder.get_object("noteBuffer")
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
        self.window = self.builder.get_object("window1")
        self.noteList = self.builder.get_object("noteList")
        self.builder.connect_signals(self)
        
        self.configFile = config
        self.listNotes = []
                
        self.repo = mypygit.Repo(self.configFile.repoLocation())
        
        self.populateNotes()
            

        
    def populateNotes(self, notes=None):
        self.noteList.clear()
        if not notes:
            #notes list was empty
            for note in self.createNoteList(self.repo.repoPath):
                self.noteList.append(note) 
        else:
            #notes list was given
            for note in notes:
                self.noteList.append([note,self.getNoteAuthor(note)])
            
            
    def createNoteList(self,repoLocation=None, list=None):
        '''
        This method will create a list within a list of [Note Filename],[Author] pairs of each of the notes within the repository.
        '''
        dir = os.listdir(repoLocation)
        listNotes = []
        for fname in dir:
            if fname[-3:] == self.configFile.session_note_extension:
                listNotes.append([fname, self.getNoteAuthor(fname)])
        return listNotes
        
            
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
    
    def searchNotes(self, entry, userData=None):
        '''
        Runs the search on the git repository
        '''
        searchString = self.builder.get_object("searchField").get_text()
        searchString = searchString.split(";")[0] # Split off any other commands that the user may have tried to tack on.
        
        #searchString = searchString.replace(' ','/ ')
        searchString = '"' + searchString + '"'
        noteList = self.repo.gitGrep(searchString)
        #for i in range (noteList.count('')):
        #    noteList.remove('')
        while (noteList.remove('')):
            pass
        
        if noteList and searchString!='':
            self.populateNotes(noteList)
        elif not noteList and searchString!= '':
            self.noteList.clear()
            
        else:
            self.populateNotes()
         
    def createConfigDialog(self):
        pass
        
        
    def sanitize(self,string):
        raise NotImplementedError
        
    def refreshNotes(self):
        raise NotImplementedError
    
    def createNote(self):
        raise NotImplementedError
    
        
                  
        
    

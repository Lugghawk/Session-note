'''
Created on 2011-08-04

@author: dl250074

http://matgnt.wordpress.com/2009/11/08/eclipse-pydev-and-gtk-with-code-completion/
'''

import sys
import configuration
import os
import mypygit
import pickle
import time

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
    
    def on_mainWindow_destroy (self, widget, data=None):
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
        note = open (self.configuration.getRepoLocation() + "\\" + str(self.get_note_name(treeview, path)))
        
        noteBuffer.set_text(note.read())
    
    def list_object_names(self):
        objects = self.builder.get_objects()
        for stuff in objects:
            print stuff
    
    def __init__(self):
        self.configFilePath = "SNote.cfg"
        if os.path.isfile(self.configFilePath):
            
            config = pickle.load(open(self.configFilePath, "r"))
        else:
            config = None
            
        self.listNotes = []
        
        #self.mainWindow.set_title(self.mainWindow.get_title() + " " + self.repo.repoPath)
        
        self.createWindows()
        if config:
            self.configuration = config
            self.repo = mypygit.Repo(self.configuration.getRepoLocation())
            self.setFieldValue("userEmailLabel", self.configuration.user_email)
            self.setFieldValue("usernameLabel", self.configuration.user_name)
            self.populateNotes()   
        else:
            self.configuration = configuration.Configuration()    
            
        if self.configuration.user_name:
            self.populateConfigDialog()
        else:
            self.doConfig()
        
        
        
        
        
    def createWindows(self):
        
        t1 = time.clock()
        #Set the gladefile
        filename = "main.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(filename)
        self.mainWindow = self.builder.get_object("mainWindow")
        filename = "config.glade"
        self.builder.add_from_file(filename)
        self.configWindow = self.builder.get_object("configWindow")
        self.configWindow.set_transient_for(self.mainWindow)
        #self.configWindow.set_visible(True)
        self.noteList = self.builder.get_object("noteList")
        self.builder.connect_signals(self)
        
        t2 = time.clock()
        print 'Window creation took %0.3f ms' % ((t2 - t1) * 1000.0)
        

            
    def doConfig(self):
        '''Show the configuration Dialog and let the user do the initial configuration'''
        self.showConfigDialog()

    def populateNotes(self, notes=None):
        self.noteList.clear()
        if not notes:
            #notes list was empty
            for note in self.createNoteList(self.repo.repoPath):
                self.noteList.append(note) 
        else:
            #notes list was given
            for note in notes:
                self.noteList.append([note, self.getNoteAuthor(note)])
            
            
    def createNoteList(self, repoLocation=None, list=None):
        '''
        This method will create a list within a list of [Note Filename],[Author] pairs of each of the notes within the repository.
        '''
        dir = os.listdir(repoLocation)
        listNotes = []
        for fname in dir:
            if fname[-3:] == self.configuration.session_note_extension:
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
            newInitials += chars + "."
            
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
        
        if noteList and searchString != '':
            self.populateNotes(noteList)
        elif not noteList and searchString != '':
            self.noteList.clear()
            
        else:
            self.populateNotes()
        
    def showConfigDialog(self, entry=None, userData=None):
        '''
        Pops up the configuration window.
        '''
        self.configWindow.set_visible(True)
        pass
    
    def hideConfigDialog(self):
        self.configWindow.set_visible(False)
    
    def saveConfigFromDialog(self, event, UserData=None):
        #Called when the 'OK' button is clicked on the configuration dialog
        #Populate the fields of self.configuration prior to writing it out to a file.
        self.configuration.user_name = self.getFieldValue("configNameField")
        self.configuration.user_email = self.getFieldValue("configEmailField")
        self.configuration.session_note_extension = self.getFieldValue("noteExtensionField")
        
        
        self.configuration.session_note_repo_location = self.getFileChooserValue("repoLocationField")
        self.configuration.text_editor_location = self.getFileChooserValue("editorPathChooser")
        self.configuration.user_note_template = self.getFileChooserValue("templateChooserButton")
        
        self.setFieldValue("userEmailLabel", self.configuration.user_email)
        self.setFieldValue("usernameLabel", self.configuration.user_name)
        
        if self.configuration.isValidConfiguration():
            self.writeConfigToPickledFile()
            self.populateNotes()
            self.hideConfigDialog()
        
    def getFileChooserValue(self, objectName):
        #Returns a uri from a FileChooser in the UI. Strips the 'file:///' from the beginning.
        return self.builder.get_object(objectName).get_uri()[8:]
    
    
    def getFieldValue(self, objectName):
        return self.builder.get_object(objectName).get_text()
    
    def setFieldValue(self, objectName, value):
        #Sets a text field value
        self.builder.get_object(objectName).set_text(value)
        
    def setFileChooserValue(self, objectName, value):
        #Sets the uri of a file chooser to the specific value
        value = "file:///" + value
        self.builder.get_object(objectName).set_uri(value)
    
    def populateConfigDialog(self):
        '''
        Populate self.configWindow items with attributes from the configuration object.
        '''
        self.setFieldValue("configNameField", self.configuration.user_name)
        self.setFieldValue("configEmailField", self.configuration.user_email)
        self.setFieldValue("noteExtensionField", self.configuration.session_note_extension)
        
        self.setFileChooserValue("repoLocationField", self.configuration.session_note_repo_location)
        self.setFileChooserValue("editorPathChooser", self.configuration.text_editor_location)
        self.setFileChooserValue("templateChooserButton", self.configuration.user_note_template)
        
        
    def cancelConfig(self, event, UserData=None):
        #print 'Cancelling config'
        if not self.configuration.isValidConfiguration():
            gtk.main_quit()
        self.hideConfigDialog()
    
    def writeConfigToPickledFile(self):
        pickleFile = open(self.configFilePath, "w")
        pickle.dump(self.configuration, pickleFile)
        pickleFile.close()
        

    def sanitize(self, string):
        raise NotImplementedError
        
    def refreshNotes(self):
        raise NotImplementedError
    
    def createNote(self):
        raise NotImplementedError
    
        
                  
        
    

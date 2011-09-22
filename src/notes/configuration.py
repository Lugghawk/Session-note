'''
Created on 2011-08-02

@author: dl250074
'''

class Configuration(object):
    '''
    This class will hold all the configuration parameters used by the program. 
    Things like repo directories, template locations, and in-template substitutes.
    
    '''
    
    known_key = 'sessionnotekey'    #Poor attempt to validate the incoming configuration file.
    user_email = ''
    user_name = ''
    
    session_note_extension = 'ses'  #The extension on the session note
    
    user_note_template = ''         #Path of the template used for notes.
    
    template_substitute_list = []   #A list of substitutes when a new note is created.
                                    #When a new note is created, we'll read from the template into a new file, and replace items in here with their counterpart values.
                                    #i.e. ["%NAME%", configuration.user_name] will replaced instances of %NAME% with the user's full name when the note is created
    
    text_editor_location = ''       #Will probably involve another subprocess call. Need to let the user know that their text editor should support a command line opening of files.
                                    #This is the editor the user will be using to open notes with.
                                    #We would like to be able to have the user open the notes by double clicking on them in the list
    session_note_repo_location = '' #Path of our local repo.
    
    session_note_remote_repo = ''   #Path of the remote repo.

    
    
    

    def __init__(self):
        '''

        '''
        
    def isValidConfiguration(self):
        if not self.user_email or not self.user_name or not self.session_note_extension or self.known_key != 'sessionnotekey':
            return False
        else:
            return True
   
    def setRepoLocation(self, location):
        self.session_note_repo_location = location
        return self.session_note_repo_location
    
    def getRepoLocation(self):
        return self.session_note_repo_location
        
        
        
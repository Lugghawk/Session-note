'''
Created on 2011-08-02

@author: dl250074
'''

class Configuration(object):
    '''
    This class will hold all the configuration parameters used by the program. 
    Things like repo directories, template locations, and in-template substitutes.
    
    '''
    user_email = ''
    user_name = ''
    user_note_template = ''
    text_editor_location = ''   # Will probably involve another subprocess call. Need to let the user know that their text editor should support a command line opening of files.
                                # This is the editor the user will be using to open notes with.
                                # We would like to be able to have the user open the notes by double clicking on them in the list
                                
    

    def __init__(self):
        '''
        This constructor will be called when no configuration file can be found.
        '''
        
        
        
'''
Created on 2011-07-15

@author: dl250074
'''
import subprocess
from os import path, mkdir, sys

class Repo(object):
    '''
    classdocs
    '''
    

    def __init__(self,):
        '''
        Constructor
        '''
        self.makeRepo()
        
    def makeRepo(self, remoterepo=''):
        '''
        Simply checking for a .git directory in the current directory
        '''
        homedir = path.expanduser("~")
        repodir = path.normcase(homedir+"/sessionnotes/")
        
                
        if not path.lexists( repodir + "/.git")  :
            if not remoterepo == '':
                print "Cloning master repo: " + self.gitClone ( repodir, remoterepo )
            else:
                print "Creating local repo: " + self.gitInit ( repodir )
        else:
            print "Git repo in" + repodir + " exists"


    def gitInit (self, repodir):
        '''
        Init the repo.
        
        This likely won't be used at all (Since clients should grab the latest version of the remote repo the first time they start, instead of creating their own).
        
        '''
        if not path.lexists ( repodir ):
            mkdir (repodir)
        cmd = 'git init'
        pipe = subprocess.Popen(cmd, shell=True, cwd=repodir)
        pipe.wait()
        
        if not path.lexists ( repodir + "/.git"):
            # Even after we run the command and wait for it to complete, the .git directory in the target repository doesn't exist.
            print "Git repo doesn't exist after 'git init' invoked. Do you not have git installed, or is it not in your path?"
            sys.exit(1) #Fail
        
        #If we don't exit in the if above, return the created repo directory
        return repodir
    
    def gitClone (self,repodir,remoterepo):
        '''
        Clone a remote repo.
        
        This should be the default behaviour. I'm not sure where the remote repo will be stored by default, but this should be configurable
        '''
        
        if not path.lexists( repodir ):
            mkdir ( repodir )
        cmd = 'git clone ' + remoterepo
        pipe = subprocess.Popen(cmd, shell=True, cwd=repodir)
        pipe.wait()
        
        if not path.lexists ( repodir + "/.git"):
            # Even after we run the command and wait for it to complete, the .git directory in the target repository doesn't exist.
            print "Git repo doesn't exist after 'git clone' invoked. Do you not have git installed, or is it not in your path?"
            sys.exit(1) #Fail

        return repodir
        
        
        
        
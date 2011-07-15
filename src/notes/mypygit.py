'''
Created on 2011-07-15

@author: dl250074
'''
import subprocess
from os import path, mkdir

class Repo(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.makeRepo()
        
    def makeRepo(self):
        '''
        Simply checking for a .git directory in the current directory
        '''
        homedir = path.expanduser("~")
        repodir = path.normcase(homedir+"/sessionnotes/")
        
        if not path.lexists( repodir + "/.git")  :
            print "Making git repo " + self.gitInit ( repodir ) 
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
        
        return repodir
    
    def gitClone (self,repodir,remoterepo):
        '''
        Clone a remote repo.
        
        This should be the default behaviour. I'm not sure where the remote repo will be stored by default, but this should be configurable
        '''
        
        
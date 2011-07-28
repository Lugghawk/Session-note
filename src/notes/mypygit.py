'''
Created on 2011-07-15

@author: Lugghawk and jenn0108

'''
import subprocess,os,platform

class Repo(object):
    '''
    classdocs
    '''
        
    gitLocation = ''
    
    def __init__(self, repopath, remoteRepo=None):
        '''
        Constructor
        '''
        print "Repo class created at " + repopath or "<no path> given"
        try:
            self.gitLocation = self.findGit()
        except IOError:
            print "Git Not Found"
            os.sys.exit(2)
            
        self.makeRepo(repopath, remoteRepo)
        
    def makeRepo(self, repopath, remoterepo=None):
        '''
        Simply checking for a .git directory in the current directory
        '''
                
        if not os.path.lexists( repopath + "/.git")  :
            if remoterepo:
                print "Cloning master repo: " + self.gitClone ( repopath, remoterepo )
            else:
                print "Creating local repo: " + self.gitInit ( repopath )
        else:
            print "Git repo in " + repopath + " exists"
            

    def gitInit (self, repodir):
        '''
        Init the repo.
        
        This likely won't be used at all (Since clients should grab the latest version of the remote repo the first time they start, instead of creating their own).
        
        '''
        if not os.path.lexists ( repodir ):
            os.mkdir (repodir)
        cmd = self.gitLocation + ' init'
        pipe = subprocess.Popen(cmd, cwd=repodir)
        pipe.wait()
        
        if not os.path.lexists ( repodir + "/.git"):
            # Even after we run the command and wait for it to complete, the .git directory in the target repository doesn't exist.
            print "Git repo doesn't exist after 'git init' invoked. Do you not have git installed, or is it not in your path?"
            os.sys.exit(1) #Fail
        
        #If we don't exit in the if above, return the created repo directory
        return repodir
    
    def gitClone (self,repodir,remoterepo):
        '''
        Clone a remote repo.
        
        This should be the default behaviour. I'm not sure where the remote repo will be stored by default, but this should be configurable
        '''
        
        if not os.path.lexists( repodir ):
            os.mkdir ( repodir )
        cmd = self.gitLocation + ' clone ' + remoterepo
        pipe = subprocess.Popen(cmd, cwd=repodir)
        pipe.wait()
        
        if not os.path.lexists ( repodir + "/.git"):
            # Even after we run the command and wait for it to complete, the .git directory in the target repository doesn't exist.
            print "Git repo doesn't exist after 'git clone' invoked. Do you not have git installed, or is it not in your path?"
            os.sys.exit(1) #Fail

        return repodir
        
        
    def findGit(self):
        if platform.system() == "Windows":
            gits = ["git.exe","git.cmd"] #Windows version of git is referenced on the command line via these files
            for gitExecutable in gits:
                gitFound = False
                for d in os.environ['PATH'].split(os.pathsep): #Split up the PATH by the seperator, ; in windows. Iterate through.
                    try:
                        fs = os.listdir(d)
                        if gitExecutable in fs:
                            gitFound = True
                            gitLocation =  os.path.join(d,gitExecutable) #Add full path to the first command element
                            break
                    except OSError:
                        pass
                if gitFound and gitExecutable == "git.exe":
                    break #Found git.exe, stop searching and use what we have.

            if gitFound and gitLocation.split("\\")[-1] == "git.cmd":
                #We found a program to run. But it's git.cmd, according to later in the code, this is an issue.
                #Copied the warning intended for this scenario.
                import warnings
                msg = "WARNING: Automatically switched to use git.cmd as git executable, which reduces performance by ~70%."
                msg += "It's recommended to put git.exe into the PATH"
                warnings.warn(msg)
            elif not gitFound:
                #Didn't find git.exe or git.cmd
                raise IOError
        return gitLocation
        
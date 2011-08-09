'''
Created on 2011-07-15

@author: Lugghawk and jenn0108

'''
import subprocess,os,platform,logging

class Repo(object):
    '''
    classdocs
    '''
        
    gitLocation = ''
    log = logging.getLogger('repolog')
    
    def __init__(self, repopath, remoteRepo=None):
        '''
        Constructor
        '''
        self.configureLogging()
        Repo.log.debug( "Repo class created at " + repopath or "<no path> given" )
        try:
            Repo.gitLocation = self.findGit()
        except IOError:
            Repo.log.critical("No git found")
            os.sys.exit(2)
        
        self.repoPath = repopath
        self.remoteRepo = remoteRepo
        
        if not self.repoExists():
            self.makeRepo()
        
            
        
    
    def configureLogging(self):
        Repo.log.addHandler(logging.StreamHandler())
        Repo.log.setLevel(logging.DEBUG)
        
    def gitGrep(self, searchString):
        '''
        Going to do case insensitive searching. And return a list of the files in the repo which contain the string.
        '''
        if searchString == '':
            return None
        cmd = 'grep -li ' + searchString
        return self.doGitCmd(cmd).split("\n")
        
        
    
    def makeRepo(self):
        '''
        Simply checking for a .git directory in the current directory
        '''
                
        if not os.path.lexists( self.repoPath + "/.git")  :
            if self.remoteRepo:
                Repo.log.debug("Cloning master repo: " + self.remoteRepo + ' to ' + self.repoPath)
                self.gitClone()
            else:
                Repo.log.debug("Creating local repo: " + self.repoPath)
                self.gitInit()
        else:
            Repo.log.info("Git repo in " + self.repopath + " exists")
            

    def gitInit (self):
        '''
        Init the repo.
        
        This likely won't be used at all (Since clients should grab the latest version of the remote repo the first time they start, instead of creating their own).
        
        '''
        if not self.checkRepoPath():
            self.makeRepoPath()
        cmd = 'init ' + self.repoPath
        self.doGitCmd(cmd)
        
        if not self.repoExists():
            # Even after we run the command and wait for it to complete, the .git directory in the target repository doesn't exist.
            Repo.log.critical( "Git repo doesn't exist after 'git init' invoked. Do you not have git installed, or is it not in your path?" )
            os.sys.exit(1) #Fail
        
        #If we don't exit in the if above, return the created repo directory
        return self.repoPath
    
    def gitClone (self):
        '''
        Clone a remote repo.
        
        This should be the default behaviour. I'm not sure where the remote repo will be stored by default, but this should be configurable
        '''
        
        if not self.checkRepoPath():
            self.makeRepoPath()
        cmd = 'clone ' + self.remoteRepo + " " + self.repoPath #Clone the repo into the repoPath directory
        self.doGitCmd(cmd)
        
        if not self.repoExists():
            # Even after we run the command and wait for it to complete, the .git directory in the target repository doesn't exist.
            Repo.log.critical( "Git repo doesn't exist after 'git clone' invoked. Do you not have git installed, or is it not in your path?" )
            os.sys.exit(1) #Fail

        return self.repoPath
    
    def gitPull(self):
        '''
        Right now this is just going to work with origin master. I may add branch support depending on whether session-note will need it (which I doubt).
        '''
        #raise NotImplementedError
        cmd = 'pull origin master'
        self.doGitCmd(cmd)
        #TODO Add support for when a pull doesn't work.
        #Potentially check the value of the self.doGitCmd() function (it returns stdout from the command) and see if there's a string we can search for.
                
    def gitPush (self):
        cmd = 'push origin master'
        self.doGitCmd(cmd)
        #TODO Add support for when a push doesn't work.
        #Potentially check the value of the self.doGitCmd() function (it returns stdout from the command) and see if there's a string we can search for.
        
    def gitStatus(self):
        '''
        This command will return to the caller a list of the entries in git status.
        It will always use the porcelain feature of git status (git status --porcelain)
        It's up to the caller to handle the output.
        '''
        
        cmd = 'status --porcelain'
        return self.doGitCmd(cmd).split("\n") # Return a list seperated by a newline.
    
    
    def doGitCmd(self, cmd):
        '''
        This method does the commands passed to it by other methods in the Repo Class.
        It does the execution of git related commands. And returns the stdout from the command.
        '''
        cmd = '"'+Repo.gitLocation+'"' + ' ' + cmd.split(";")[0] #Split off any additional commands that may have gotten in.
        Repo.log.debug("Command Executed: " + cmd)
        pipe = subprocess.Popen(cmd, cwd=self.repoPath, stdout=subprocess.PIPE)
        pipe.wait()
        return pipe.stdout.read()
    
    def makeRepoPath(self):
        try:
            os.mkdir(self.repoPath)
        except WindowsError:
            pass # directory already exists.
    
    def checkRepoPath(self):
        if os.path.lexists(self.repoPath):
            return True
        else:
            return False
    
    def repoExists(self):
        return os.path.lexists ( self.repoPath + "/.git")
    
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
                msg = "WARNING: Automatically switched to use git.cmd as git executable, which reduces performance by ~70%."
                msg += "It's recommended to put git.exe into the PATH"
                Repo.log.warning(msg)
            elif not gitFound:
                #Didn't find git.exe or git.cmd
                raise IOError
        return gitLocation
        
'''
Created on 2011-07-15

@author: Lugghawk and jenn0108
'''

if __name__ == '__main__':
    pass

import os, mypygit

homedir = os.path.expanduser("~")
repodir = os.path.normcase(homedir+"/sessionnotes/")

remoteRepoDir = os.path.normcase(r"C:\SessionNotes\repo")

repo = mypygit.Repo(repodir, remoteRepoDir)
'''
Created on 2011-07-15

@author: Lugghawk and jenn0108
'''

import os, mypygit,sys, ui,configuration

'''homedir = os.path.expanduser("~")
repodir = os.path.normcase(homedir+"/sessionnotes/")

remoteRepoDir = os.path.normcase(r"C:\SessionNotes\repo")

#repo = mypygit.Repo(repodir, remoteRepoDir)
'''

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
  
config = configuration.Configuration()
config.setRepoLocation(os.path.normcase ("C:/SessionNotes/repo"))
myUI = ui.UI(config)
gtk.main()
    
    
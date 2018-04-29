"""
    This file contains all the constant variables for GUI
    This includes things like:
    1. Directory and file paths
"""

import os


allowedImageExtensions = [ "png", "jpeg", "jpg" ]
DirTreeAllowedFileTypes = [ "png", "jpeg", "jpg", "html", "css", "js" ]
path_root = os.curdir
path_configs = os.path.join( path_root, "Configs" )
path_icons = os.path.join( path_root, "Resources", "Icons" )
maxCount_RecentProjects = 4

settingsFileName = "__settings__.wf2html"


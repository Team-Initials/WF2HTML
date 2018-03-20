"""
    This file automates the process of generating .py files from .ui files
    ** It is not of relevant use to the actual project
"""

import os

ui_directory = "ui_designer"
listOfUi = os.listdir( ui_directory )

for ui in listOfUi:
    srcPath = os.path.join( ui_directory, ui )
    destFile = "Ui_" + ".".join( ui.split(".")[:-1] ) + ".py"
    destPath = os.path.join( "ui_py", destFile )
    command = "pyside-uic " + srcPath + " > " + destPath
    print command
    os.system( command )
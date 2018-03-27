"""
    This is an API file which creates log messages
    Which will be displayed in different parts of the GUI
"""

from datetime import datetime


def _insertDatetime( message ):
    return str( datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : " + message )


def _prepareMessageForDisplay( message ):
    message = _insertDatetime( message )
    return message


def msgNormal( message ):
    return _prepareMessageForDisplay( message )


def msgUnsupportedFiletype( filePath ):
    extension = filePath.split( "." )[ -1 ]
    message = "The filetype '."+ extension +"' is not supported in this scenario."
    return _prepareMessageForDisplay( message )


def msgOpenedProject( projectPath ):
    message = "Opened the project '"+ projectPath +"'."
    return _prepareMessageForDisplay( message )


def msgAddedDirectory( directoryName ):
    message = "Added the directory '" + directoryName + "'."
    return _prepareMessageForDisplay( message )

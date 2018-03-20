"""
    The function in this file deals with all kinds of functions related to file like:
    Validating a file type, creating, copying, deleting files and directories
"""

import os
import Constants


def splitPaths( path ):
    pathList = list( os.path.split( path ) )
    lastVal = pathList[ 0 ]
    while True:
        tempSplit = list( os.path.split( pathList[0] ) )
        if not tempSplit[ 1 ]:
            break
        pathList = tempSplit + pathList[1:]
    return pathList


def mkdir_p( path ):
    pathParts = splitPaths( path )
    path = ""
    for dir in pathParts:
        path = os.path.join( path, dir )
        if not os.path.isdir( path ):
            os.mkdir( path )


def getFileExtension( filePath ):
    fileName = os.path.basename( filePath )
    fileNameComponents = fileName.split( "." )
    extension = ""
    if len( fileNameComponents ) >= 1:
        extension = fileNameComponents[ -1 ]
    return extension


def isValidImageFile( filePath ):
    extension = getFileExtension( filePath )
    if extension.lower() in Constants.allowedImageExtensions:
        return True
    return False


def isNonEmptyDir( itemPath ):
    if not os.path.isdir( itemPath ):
        return False
    if len(os.listdir( itemPath )) == 0:
        return False
    return True


def changeExtension( filePath, targetExtension ):
    fileName = os.path.basename( filePath )
    fileDir = os.path.dirname( filePath )
    fileNameComponents = fileName.split(".")
    if len( fileNameComponents ) >= 1:
        fileNameComponents = fileNameComponents[:-1]
    newFileName = ".".join(fileNameComponents) + "." + targetExtension
    return os.path.join( fileDir, newFileName )


def readFileContent( filePath ):
    with open(filePath, "r") as file:
        content = file.read()
    return content


def writeToFile( content, filePath ):
    with open(filePath, "w") as file:
        file.write( content )
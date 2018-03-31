"""
    This deals with projcets like:
    opening projects
    deleting projects
    managing project settings
    adding files to projects
    removing files from projects
"""

import os
import json
import shutil
import Constants

from datetime import datetime
from API import FileManagers

path_createdProjects = os.path.join( Constants.path_configs, "createdProjects.json" )


def _getCreatedProjectsJson():

    if not os.path.isdir( Constants.path_configs ):
        return None

    if not os.path.isfile( path_createdProjects ):
        return None

    with open( path_createdProjects, "r" ) as jsonFile:
        try:
            projects = json.load( jsonFile )
        except Exception as e:
            print e
            return None

    return projects


def _updateCreatedProjectsJson( projects=list() ):
    if not os.path.isdir( Constants.path_configs ):
        os.mkdir( Constants.path_configs )

    with open( path_createdProjects, "w" ) as jsonFile:
        try:
            json.dump( projects, jsonFile )
        except Exception as e:
            print e
            return False

    return True


def _removeProjectDirectory( projectPath ):
    if os.path.isdir( projectPath ):
        shutil.rmtree( projectPath )


def _removeProjectFromJson( projectPath ):
    projects = _getCreatedProjectsJson()
    if not projects:
        return

    temp_projects = []
    for project in projects:
        if project["path"] != projectPath:
            temp_projects.append( project )

    _updateCreatedProjectsJson( temp_projects )


def isValidProjectPath( projectPath ):
    if not projectPath:
        return False
    return True


def isUsedProjectPath( projectPath ):
    """ Check the projects.json file to check if this path is being used currently """

    projects = _getCreatedProjectsJson()

    if not projects:
        return False

    for project in projects:
        if project["path"] == projectPath:
            return True

    return False


def _saveProjectToJson( projectPath ):
    # Json Structure:
    timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
    currentProjectJson = { "name": os.path.basename( projectPath ),
                           "path": projectPath,
                           "timestamp": str( timestamp )
                           }

    projects = _getCreatedProjectsJson()
    if not projects:
        projects = []

    for project in projects:
        if project["path"] == projectPath:
            break
    else:
        projects.append( currentProjectJson )

    return _updateCreatedProjectsJson( projects )


def createProject( projectPath ):

    projectCreationErrors = None

    if not projectPath:
        projectCreationErrors = "'"+ projectPath +"' is not a valid project path."
        return projectCreationErrors

    if not os.path.isdir( projectPath ):
        os.mkdir( projectPath )

    settingsFile = open( os.path.join(projectPath, "__settings__.wf2html"), "w" )
    settingsFile.close()

    if not _saveProjectToJson( projectPath ):
        projectCreationErrors = "Could not update the JSON file for projects."
        deleteProject( projectPath )

    return projectCreationErrors


def validateCreatedProjects():
    projects = _getCreatedProjectsJson()
    if not projects:
        return
    validatedProjects = []
    for project in projects:
        if project["path"] and os.path.exists(project["path"]):
            validatedProjects.append( project )
    _updateCreatedProjectsJson( validatedProjects )


def deleteProject( projectPath ):
    _removeProjectDirectory( projectPath )
    _removeProjectFromJson( projectPath )


def getRecentProjects():
    projects = _getCreatedProjectsJson()
    if not projects:
        return None

    timestamps = [ (index, float( project["timestamp"])) for index, project in enumerate( projects ) ]
    timestamps.sort( key=lambda x:x[1], reverse=True )

    latestTimestamps = timestamps[ 0 : Constants.maxCount_RecentProjects ]
    result = []

    for timestampTuple in latestTimestamps:
        result.append( { "name": projects[ timestampTuple[0] ]["name"], "path": projects[ timestampTuple[0] ]["path"] } )

    return result


def openProject( projectPath ):
    projects = _getCreatedProjectsJson()
    if not projects:
        return

    temp_projects = []
    for project in projects:
        temp = project
        if project["path"] == projectPath:
            temp["timestamp"] = str( (datetime.now() - datetime(1970, 1, 1)).total_seconds() )
        temp_projects.append( temp )

    _updateCreatedProjectsJson( temp_projects )


def copyImageToProject( srcPath, destPath, filename ):
    FileManagers.mkdir_p( destPath )
    shutil.copy( os.path.join( srcPath, filename),
                 os.path.join( destPath, filename))

def addDirectoryInProject( parentDirectory, newDirectoryName ):
    try:
        os.mkdir( os.path.join( parentDirectory, newDirectoryName ) )
    except Exception as e:
        print e
        return { "status": False,
                 "message": e }
    else:
        return { "status": True }


def removeItemFromProject( itemPath ):
    if os.path.isdir( itemPath ):
        shutil.rmtree( itemPath )
    else:
        os.remove( itemPath )

def isValidWF2HTMLProject( projectPath ):
    allProjectInJson = _getCreatedProjectsJson()
    allProjectPaths = [ project["path"] for project in allProjectInJson ]
    if not projectPath in allProjectPaths:
        return False

    if not os.path.exists( os.path.join( projectPath, "__settings__.wf2html") ):
        return False

    return True
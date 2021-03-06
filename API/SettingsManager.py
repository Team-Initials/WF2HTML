"""
 Contains stuff related to settings for a project
"""

import json
import os

import Constants

defaultSettings = [
    # CSS Tab
    {
        "tabName": "CSS",
        "contents": [
            # CSS type selector
            {
                "id": "css-type",
                "name": "Select the type of CSS you want",
                "inputType": "comboBox",
                "inputTypeDetails": {
                    "possibleValues": ["External", "Internal", "Inline"],
                    "currentIndex": 0,
                },
            }
        ],
    },

    # General Tab
    {
        "tabName": "General",
        "contents": [
            {
                "id": "multiple-image-layout",
                "name": "Layout for multiple images",
                "inputType": "comboBox",
                "inputTypeDetails": {
                    "possibleValues": ["Vertical", "Horizontal"],
                    "currentIndex": 0,
                },
            }
        ]
    }
]


# Paths to modify the values when the value is changed from UI
idValuePaths = {
    "css-type": "0.contents.0.inputTypeDetails",
    "multiple-image-layout": "1.contents.0.inputTypeDetails"
}

def _getPathValue( settings, path ):
    if len(path) == 0:
        return None
    if len(path) == 1:
        return settings[ path[0] ]
    else:
        return _getPathValue( settings[ path[0] ], path[1:] )


def _writeSettingsFile( settingsPath, settings ):
    with open( settingsPath, "w" ) as jsonFile:
        try:
            json.dump( settings, jsonFile )
        except Exception as e:
            print e


def getProjectSettings( projectPath ):
    with open( os.path.join( projectPath, Constants.settingsFileName), "r") as jsonFile:
        try:
            settings = json.load(jsonFile)
        except Exception as e:
            print e
            return defaultSettings
        else:
            return settings


def generateDefaultSettings( projectPath ):
    _writeSettingsFile( os.path.join( projectPath, Constants.settingsFileName ), defaultSettings )

def updateProjectSettings( projectPath, settings ):
    _writeSettingsFile(os.path.join(projectPath, Constants.settingsFileName), settings)

def getCssType( projectPath ):
    settings = getProjectSettings( projectPath )
    path = idValuePaths["css-type"].split(".")
    path = [ int(item) if item.isdigit() else item for item in path ]
    index = _getPathValue( settings, path + ["currentIndex"] )
    return _getPathValue( settings, path + ["possibleValues"])[ index ]

def getMultipleImageLayoutDirection( projectPath ):
    settings = getProjectSettings(projectPath)
    path = idValuePaths["multiple-image-layout"].split(".")
    path = [int(item) if item.isdigit() else item for item in path]
    index = _getPathValue(settings, path + ["currentIndex"])
    return _getPathValue(settings, path + ["possibleValues"])[index]
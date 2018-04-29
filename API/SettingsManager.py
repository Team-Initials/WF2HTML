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
    "css-type": "0.contents.0.inputTypeDetails.currentIndex",
    "multiple-image-layout": "1.contents.0.inputTypeDetails.currentIndex"
}


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
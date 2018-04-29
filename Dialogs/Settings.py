"""
    Contains everything required to manipulate the settings dialog page
"""

import sys
import copy
from PySide import QtCore, QtGui
from API import SettingsManager

class SettingsDialog(QtGui.QDialog):
    def __init__(self, projectPath, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.resize( 400, 600)

        # Prevents user from accessing the mainWindow when the Dialog is open
        self.setWindowModality( QtCore.Qt.WindowModal )

        self.setFixedSize( self.size() )

        self.projectPath = projectPath

        self.vbox = QtGui.QVBoxLayout( self )
        self.tabWidget = QtGui.QTabWidget()

        self.projectSettings = copy.deepcopy( SettingsManager.getProjectSettings( self.projectPath ) )

        self.tabs = []
        for tabDetails in self.projectSettings:
            tab = QtGui.QWidget()
            self.tabs.append( tab )

            vBox_tab = QtGui.QVBoxLayout( tab )
            vBox_tab.setContentsMargins(0, 0, 0, 0)
            scrollArea = QtGui.QScrollArea( tab )

            scrollAreaContents = QtGui.QWidget()
            formLayout = QtGui.QFormLayout( scrollAreaContents )

            tabOptions = tabDetails["contents"]
            for row, option in enumerate(tabOptions):
                label = QtGui.QLabel()
                label.setText( option["name"] )
                label.setAlignment(QtCore.Qt.AlignLeft)
                label.setFixedWidth( 95 )
                label.setWordWrap( True )

                inputField = self.generateInputField( inputType=option["inputType"],
                                                      inputTypeDetails=option["inputTypeDetails"],
                                                      fieldId=option["id"] )
                formLayout.setWidget( row, QtGui.QFormLayout.LabelRole, label )
                formLayout.setWidget( row, QtGui.QFormLayout.FieldRole, inputField )

            # tab.setLayout( vBox_tab )
            self.tabWidget.addTab(tab, tabDetails["tabName"])
            scrollArea.setWidget( scrollAreaContents )
            vBox_tab.addWidget( scrollArea )


        self.vbox.addWidget( self.tabWidget )


        self.buttonBox = QtGui.QDialogButtonBox( self )
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Save)

        self.vbox.addWidget( self.buttonBox )

        self.setLayout( self.vbox )
        self.setWindowTitle( "Settings" )

        self.buttonBox.accepted.connect(self.saveSettings)
        self.buttonBox.rejected.connect(self.cancelSettings)

    def generateInputField(self, inputType, fieldId, inputTypeDetails=None):
        inputField = None
        if inputType=="comboBox":
            inputField = QtGui.QComboBox()
            for value in inputTypeDetails["possibleValues"]:
                inputField.addItem( value )
            inputField.setCurrentIndex( inputTypeDetails["currentIndex"] )
            inputField.setFixedWidth( 250 )
            inputField.currentIndexChanged.connect(lambda: self._updateInternalSettings(fieldId,
                                                                                        inputField,
                                                                                        fieldType="comboBox"))
        return inputField

    def _updateValue(self, settings, path, value):
        if len(path) == 0:
            return
        if len(path) == 1:
            settings[ path[0] ] = value
        else:
            self._updateValue( settings[ path[0] ], path[1:], value )

    def _updateInternalSettings(self, id, inputField, fieldType ):
        value = None
        if fieldType=="comboBox":
            value = inputField.currentIndex()
        if value != None and id in SettingsManager.idValuePaths:
            path = SettingsManager.idValuePaths[ id ]
            path = path.split(".")
            path = [ int(item) if item.isdigit() else item for item in path ]
            self._updateValue( self.projectSettings, path, value )

    def saveSettings(self):
        SettingsManager.updateProjectSettings(projectPath=self.projectPath, settings=self.projectSettings )
        self.accept()

    def cancelSettings(self):
        self.reject()

#!/usr/bin/env python

"""
    This file is the starting point of the program.
    Run this file from the command prompt using python.py

    Packaging this project:
    1. Open a command prompt
    2. cd into the folder "Project"
    3. run the command "pyinstaller execute.py"

    ** NOTE: The line "from PySide import QtXml" must be present for pyinstaller to work properly on this function.
"""
import os
import sys

from PySide import QtCore, QtGui, QtWebKit
from PySide.QtCore import Slot
from PySide.QtWebKit import QWebFrame


import Constants
from API import FileManagers, Loggers, ProjectManagers, ImageProcessors, HtmlGenerators, SystemCommands, SettingsManager
from API import HtmlManager
from Designs.ui_py import Ui_MainWindow
from Dialogs import Settings

# Importing PySide.QtXml for packaging purposes
# pyinstaller could not detect it otherwise, and builds failed
from PySide import QtXml


# Class for the Split Screen Display Window
class SplitScreenDialog(QtGui.QDialog):
    def __init__(self, htmlFilePath, cssFilePath, parent=None):
        super(SplitScreenDialog, self).__init__(parent)
        # Prevents user from accessing the mainWindow when the Dialog is open
        self.currentHtmlPath = htmlFilePath
        self.currentCssPath = cssFilePath

        self.hbox = QtGui.QHBoxLayout( self )

        self.splitter_H = QtGui.QSplitter( QtCore.Qt.Horizontal )
        self.splitter_V = QtGui.QSplitter(QtCore.Qt.Vertical)

        self.textEdit_htmlDisplay = QtGui.QPlainTextEdit( self )
        self.textEdit_htmlDisplay.setReadOnly( False )
        self.textEdit_htmlDisplay.setPlainText( FileManagers.readFileContent( self.currentHtmlPath ))
        self.textEdit_htmlDisplay.textChanged.connect(self.updateHtml)
        self.splitter_V.addWidget(self.textEdit_htmlDisplay)

        if cssFilePath != None:
            self.textEdit_cssDisplay = QtGui.QPlainTextEdit( self )
            self.textEdit_cssDisplay.setReadOnly( False )
            self.textEdit_cssDisplay.setPlainText( FileManagers.readFileContent( self.currentCssPath ))
            self.textEdit_cssDisplay.textChanged.connect(self.updateCss)
            self.splitter_V.addWidget( self.textEdit_cssDisplay )

        self.webView = QtWebKit.QWebView()
        self.webFrame = self.webView.page().mainFrame()
        self.webView.load( QtCore.QUrl.fromLocalFile( self.currentHtmlPath ) )

        self.splitter_H.addWidget( self.splitter_V )
        self.splitter_H.addWidget( self.webView )

        self.hbox.addWidget( self.splitter_H )
        self.setLayout( self.hbox )

        self.setWindowTitle( 'Web Preview' )

    def updateHtml( self ):
        text = self.textEdit_htmlDisplay.toPlainText()
        FileManagers.writeToFile( text, self.currentHtmlPath )

    def updateHtmlCode(self):
        currentText = FileManagers.readFileContent(self.currentHtmlPath)
        self.textEdit_htmlDisplay.clear()
        self.textEdit_htmlDisplay.setPlainText( currentText )
        self.refreshWebView()

    def updateCss( self ):
        text = self.textEdit_cssDisplay.toPlainText()
        FileManagers.writeToFile( text, self.currentCssPath )
        self.webView.reload()

    def refreshWebView(self):
        self.webView.deleteLater()
        self.webView = QtWebKit.QWebView()
        self.webFrame = self.webView.page().mainFrame()
        self.webView.load(QtCore.QUrl.fromLocalFile(self.currentHtmlPath))
        self.splitter_H.addWidget(self.webView)
        # self.webView.reload()
        # self.webView.repaint()
        # self.webView.update()

class MainWindow(QtGui.QMainWindow, Ui_MainWindow.Ui_MainWindow):
    currentProjectPath = None
    currentImageShownPath = None
    currentFolderShown = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi( self )
        #self.showMaximized()

        # Validate and clear the json file of invalid paths
        ProjectManagers.validateCreatedProjects()

        # Add 4 most recent projects to the Recent Project menu option
        self.updateRecentProjects()

        self.pixmapLabels = []

        # Adding event listeners
        self.actionNew_Image.triggered.connect( self.addImage )
        self.actionClear_Log.triggered.connect( self.clearLog )
        self.actionNew_Project.triggered.connect( self.createAndOpenProject )
        self.actionSettings.triggered.connect( self.displaySettings )
        self.actionConvert_showInDialog.triggered.connect( self.convertCurrentImage_Dialog )
        self.actionConvert_showInBrowser.triggered.connect( self.converCurrentImage_Browser )
        self.actionEdit_MsPaint.triggered.connect( self.editImageMsPaint )
        self.actionRefresh_Image.triggered.connect( self.refreshImage )
        self.actionOpen_Project.triggered.connect( self.openWF2HTMLProject )

        # Try and open last project
        self.openLastProject()

    # =================================================================================================================
    # Displaying Settings

    def displaySettings(self):
        if self.currentProjectPath:
            self.settingsDialog = Settings.SettingsDialog( projectPath=self.currentProjectPath, parent=self )
            self.settingsDialog.show()
        else:
            self.logError( message=Loggers.msgNormal("A project must be opened before editing its settings.") )

    # =================================================================================================================
    # Editing

    def refreshImage( self ):
        if not self.currentImageShownPath:
            #TODO: Log that no image is chosen currently
            return
        self.showImage( imagePath=self.currentImageShownPath )

    def editImageMsPaint( self ):
        if not self.currentImageShownPath:
            #TODO: Log that no image is chosen currently
            return
        command = SystemCommands.SystemCommands["defaultImgEditor"][os.name] + " '" + self.currentImageShownPath + "'"
        os.system( command )

    # =================================================================================================================

    # =================================================================================================================
    # Managing image conversion

    def convertCurrentImage( self ):
        if not self.currentFolderShown:
            self.logError( Loggers.msgNormal( "No image is open currently. An image should be open for conversion." ) )
            return
        allWireFrameData = list()
        startingDivIndex = 1
        for image in ProjectManagers.getImagesInDirectory( self.currentFolderShown ):
            wireFrameData, elementCount = ImageProcessors.getWireframeDataFromImage(
                                                    imageFilePath=os.path.join( self.currentFolderShown, image ),
                                                    startingDivIndex=startingDivIndex)
            startingDivIndex = startingDivIndex + elementCount
            allWireFrameData.append( wireFrameData )

        cssType = SettingsManager.getCssType( self.currentProjectPath )
        HtmlGenerators.generateHtmlFromWireframeData( allWireFrameData,
                                                      imageFilePath=self.currentImageShownPath,
                                                      cssType=cssType,
                                                      imageLayoutDirection=SettingsManager.getMultipleImageLayoutDirection(self.currentFolderShown))

    def showSplitScreenPreview( self, htmlFilePath, cssFilePath ):
        self.splitScreenDialog = SplitScreenDialog( parent=self, htmlFilePath=htmlFilePath, cssFilePath=cssFilePath )
        self.splitScreenDialog.webFrame.addToJavaScriptWindowObject('WebViewController', self)
        self.splitScreenDialog.show()

    def convertCurrentImage_Dialog( self ):
        self.convertCurrentImage()
        self.generateDirTree()
        cssFilePath = None
        htmlFilePath = FileManagers.changeExtension( self.currentImageShownPath, "html" )
        if SettingsManager.getCssType( self.currentProjectPath) == "External":
            cssFilePath = FileManagers.changeExtension( self.currentImageShownPath, "css" )
        self.showSplitScreenPreview( htmlFilePath, cssFilePath )

    def converCurrentImage_Browser( self ):
        self.convertCurrentImage()
        self.generateDirTree()
        htmlFilePath = FileManagers.changeExtension(self.currentImageShownPath, "html")
        self.showPageInBrowser( htmlFilePath )

    def showPageInBrowser( self, htmlFilePath ):
        command = SystemCommands.SystemCommands["defaultBrowser"][os.name] + " '" + htmlFilePath + "'"
        os.system( command )

    # =================================================================================================================
    # Managing recent Projects

    def updateRecentProjects( self ):
        recentProjects = ProjectManagers.getRecentProjects()
        self.menuOpen_Recent_Project.clear()
        if recentProjects:
            self.addRecentProjects( recentProjects )
        else:
            self.actionNo_recent_projects = QtGui.QAction( "No recent projects", self.menuOpen_Recent_Project )
            self.menuOpen_Recent_Project.addAction( self.actionNo_recent_projects )

    def addRecentProjects( self, recentProjects ):
        self.menuOpen_Recent_Project.clear()
        self.recentProjectActions = dict()
        for index, project in enumerate( recentProjects ):
            self.recentProjectActions[ index ] = QtGui.QAction( project["path"], self.menuOpen_Recent_Project )
            self.recentProjectActions[ index ].triggered.connect( self.openRecentProject )
            self.menuOpen_Recent_Project.addAction( self.recentProjectActions[index] )

    # ==================================================================================================================
    # Managing directory tree context menu

    def getDirTreeFilePath( self, dirTreeItem ):
        if not dirTreeItem:
            return self.currentProjectPath

        dirTreeFilePath = os.path.join( self.getDirTreeDirectoryPath( dirTreeItem.parent() ), dirTreeItem.text( 0 ) )
        return dirTreeFilePath

    def getDirTreeDirectoryPath( self, dirTreeItem ):
        dirTreeDirPath = self.getDirTreeFilePath( dirTreeItem )
        if not os.path.isdir( dirTreeDirPath ):
            dirTreeDirPath = os.path.abspath( os.path.dirname( dirTreeDirPath ) )
        return dirTreeDirPath

    # TODO: Make context menu options decativatable based on item type
    def addDirTreeContextMenu( self ):
        listOfActions = [ action.text() for action in self.treeWidget_dirTree.actions() ]
        if not "Add Image" in listOfActions:
            contextAction_addImage = QtGui.QAction( "Add Image", self.treeWidget_dirTree )
            self.treeWidget_dirTree.addAction( contextAction_addImage )
            contextAction_addImage.triggered.connect( lambda: self.dirTreeAddImage(
                                                                self.treeWidget_dirTree.currentItem(), type="single"))
        if not "Add Multiple Images" in listOfActions:
            contextAction_addMultImage = QtGui.QAction( "Add Multiple Images", self.treeWidget_dirTree )
            self.treeWidget_dirTree.addAction( contextAction_addMultImage )
            contextAction_addMultImage.triggered.connect( lambda: self.dirTreeAddImage(
                                                                self.treeWidget_dirTree.currentItem(), type="multiple" ))
        if not "Add Directory" in listOfActions:
            contextAction_addImage = QtGui.QAction( "Add Directory", self.treeWidget_dirTree )
            self.treeWidget_dirTree.addAction( contextAction_addImage )
            contextAction_addImage.triggered.connect( lambda: self.dirTreeAddDirectory(
                                                                        self.treeWidget_dirTree.currentItem() ))
        if not "Delete" in listOfActions:
            contextAction_addImage = QtGui.QAction( "Delete", self.treeWidget_dirTree )
            self.treeWidget_dirTree.addAction( contextAction_addImage )
            contextAction_addImage.triggered.connect( lambda: self.dirTreeDeleteItem(
                                                                        self.treeWidget_dirTree.currentItem() ))

    def dirTreeAddImage( self, currentItem, type="single" ):
        directoryPath =  self.getDirTreeDirectoryPath( currentItem )
        self.addImage( directoryPath=directoryPath, type=type )

    def dirTreeAddDirectory( self, currentItem ):
        parentDirectoryPath =  self.getDirTreeDirectoryPath( currentItem )
        newDirName, haveReceivedName = QtGui.QInputDialog.getText( self, "Enter Directory Name",
                                                    """ Enter the new Directory Name: """)
        if haveReceivedName:
            self.addDirectory( parentDirectoryPath, newDirName )

    def dirTreeDeleteItem( self, currentItem ):
        if currentItem is self.treeWidget_dirTree.topLevelItem( 0 ):
            self.deleteProject()
        else:
            itemPath = self.getDirTreeFilePath( currentItem )
            self.deletePath( itemPath )

    # ==================================================================================================================
    # Managing the directory tree on the left

    def addFolderContentsDirTree( self, folderPath, treeParentNode ):
        folderContents = os.listdir( folderPath )
        for content in folderContents:
            contentPath = os.path.join( folderPath, content )
            if not os.path.isdir(contentPath) \
                    and not FileManagers.getFileExtension(contentPath).lower() in Constants.DirTreeAllowedFileTypes:
                continue

            treeNode = QtGui.QTreeWidgetItem()
            treeNode.setText( 0, content )
            if os.path.isdir( contentPath ):
                treeNode.setIcon(0, QtGui.QIcon( os.path.join( Constants.path_icons, "folder.png" ) ) )
            else:
                treeNode.setIcon(0, QtGui.QIcon( os.path.join( Constants.path_icons, "file_img.png" ) ) )
            treeParentNode.addChild( treeNode )

            if os.path.isdir( contentPath ):
                self.addFolderContentsDirTree( contentPath, treeNode )

    def generateDirTree( self ):
        projectPath = self.currentProjectPath

        self.treeWidget_dirTree.clear()

        dirTreeTopLevelItem = QtGui.QTreeWidgetItem()
        dirTreeTopLevelItem.setIcon( 0, QtGui.QIcon( os.path.join( Constants.path_icons, "folder.png")) )
        dirTreeTopLevelItem.setText( 0, os.path.basename( projectPath ) )

        self.treeWidget_dirTree.addTopLevelItem( dirTreeTopLevelItem )

        self.addFolderContentsDirTree( projectPath, dirTreeTopLevelItem )
        self.treeWidget_dirTree.itemDoubleClicked.connect( lambda: self.dirTreeOpenImage(
                                                                        self.treeWidget_dirTree.currentItem() ))
        self.treeWidget_dirTree.setContextMenuPolicy( QtCore.Qt.ActionsContextMenu )
        self.addDirTreeContextMenu()

    def insertPathInDirTree( self, parentNode, path, type ):
        if len( path ) == 1:
            childNode = QtGui.QTreeWidgetItem()
            childNode.setText( 0, path[0] )
            if type=="dir":
                childNode.setIcon(0, QtGui.QIcon( os.path.join( Constants.path_icons, "folder.png" ) ) )
            else:
                childNode.setIcon(0, QtGui.QIcon( os.path.join( Constants.path_icons, "file_img.png" ) ) )
            parentNode.addChild( childNode )
            return

        childCount = parentNode.childCount()
        for index in xrange( childCount ):
            child = parentNode.child( index )
            if child.text( 0 ) == path[0]:
                self.insertPathInDirTree( parentNode=child, path=path[1:], type=type)
                break

    def removePathFromDirTree( self, parentNode, path ):
        if len( path ) == 1:
            childCount = parentNode.childCount()
            for index in xrange( childCount ):
                child = parentNode.child( index )
                if child.text( 0 ) == path[ 0 ]:
                    parentNode.removeChild( child )
                    break
            return

        childCount = parentNode.childCount()
        for index in xrange( childCount ):
            child = parentNode.child( index )
            if child.text( 0 ) == path[0]:
                self.removePathFromDirTree( parentNode=child, path=path[1:])
                break

    def removeItemFromDirTree( self, itemPath ):
        pathComponents = FileManagers.splitPaths( itemPath )
        rootPathComponents = FileManagers.splitPaths( self.currentProjectPath )
        path = pathComponents[ len( rootPathComponents ): ]

        topLevelItem = self.treeWidget_dirTree.topLevelItem( 0 )
        self.removePathFromDirTree( parentNode=topLevelItem, path=path )

    def updateDirTree( self, path ):
        if os.path.isdir( path ):
            type = "dir"
        else:
            type = "file"
        pathComponents = FileManagers.splitPaths( path )
        rootPathComponents = FileManagers.splitPaths( self.currentProjectPath )
        path = pathComponents[ len(rootPathComponents): ]

        topLevelItem = self.treeWidget_dirTree.topLevelItem( 0 )
        self.insertPathInDirTree( parentNode=topLevelItem, path=path, type=type )

    # ==================================================================================================================
    # Opening Project

    def dirTreeOpenImage( self, currentItem ):
        path = self.getDirTreeFilePath( currentItem )
        if FileManagers.isValidImageFile( path ):
            self.showImage( path )

    def openProject( self, projectPath ):
        if self.currentProjectPath:
            confirmOpen = QtGui.QMessageBox.question( self, "Confirm Open",
                                                           "A project is already open. Close it to open the new one ?",
                                                           QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel )
            if confirmOpen == QtGui.QMessageBox.Cancel:
                return
        self.currentProjectPath = projectPath
        self.setWindowTitle( projectPath )
        ProjectManagers.openProject( projectPath )
        self.logSuccess( Loggers.msgOpenedProject( projectPath ) )
        self.generateDirTree()
        self.clearImageView()
        self.updateRecentProjects()

    def openLastProject( self ):
        recentProjects = ProjectManagers.getRecentProjects()
        if not recentProjects:
            return
        else:
            self.openProject( projectPath=recentProjects[0]["path"])

    def openRecentProject( self ):
        projectPath = self.sender().text()
        self.openProject( projectPath )

    def createAndOpenProject( self ):
        projectPath = QtGui.QFileDialog.getExistingDirectory( self, "Choose Project Directory" )

        # This is a check for whether cancel button was clicked
        if projectPath.strip() == "" or projectPath == None:
            self.log( Loggers.msgNormal( "The project creation was cancelled." ) )
            return

        if ProjectManagers.isUsedProjectPath( projectPath=projectPath ):
            # Show a popup asking if the user wants to overwrite an old project
            confirmOverwrite = QtGui.QMessageBox.question( self, "Confirm Overwrite",
                                                 "A project already exists at that path. Do you want to overwrite it?",
                                                 QtGui.QMessageBox.Yes|QtGui.QMessageBox.No )
            if confirmOverwrite == QtGui.QMessageBox.No:
                self.log( Loggers.msgNormal( "The project creation was cancelled." ) )
                return
            elif confirmOverwrite == QtGui.QMessageBox.Yes:
                ProjectManagers.deleteProject( projectPath )

        projectCreationErrors = ProjectManagers.createProject( projectPath )
        if not projectCreationErrors:
            self.logSuccess( Loggers.msgNormal( "Successfully created the project" ) )
            self.openProject( projectPath )
        else:
            self.logError( Loggers.msgNormal( projectCreationErrors ) )

    def openWF2HTMLProject( self ):
        projectPath = QtGui.QFileDialog.getExistingDirectory( self, "Select Project" )

        # This is a check for whether cancel button was clicked
        if projectPath.strip() == "" or projectPath == None:
            self.log( Loggers.msgNormal( "The project opening was cancelled." ) )
            return

        if not ProjectManagers.isValidWF2HTMLProject( projectPath=projectPath ):
            self.logError( Loggers.msgNormal( "The directory is not a WF2HTML project. Either it was not created using this application, or the '__settings__.wf2html' file is missing" ))
            return
        self.openProject( projectPath )

    # ==================================================================================================================
    # Adding things to project

    def addDirectory( self, parentDirectory, newDirectoryName ):
        addingDirectory = ProjectManagers.addDirectoryInProject( parentDirectory, newDirectoryName )
        if addingDirectory[ "status" ]:
            self.logSuccess( Loggers.msgAddedDirectory( newDirectoryName) )
            self.updateDirTree( os.path.join( parentDirectory, newDirectoryName ) )
        else:
            self.logError( Loggers.msgNormal( addingDirectory["message"] ) )


    def showImage( self, imagePath ):
        self.clearImageView()
        if not imagePath:
            return
        # Setting the global variables
        self.currentImageShownPath = imagePath
        self.currentFolderShown = os.path.dirname(imagePath)

        # Setting up the layout
        self.imageDisplayAreaContents = QtGui.QWidget()
        multipleImageLayoutDirection = SettingsManager.getMultipleImageLayoutDirection( self.currentProjectPath )
        if multipleImageLayoutDirection == "Vertical":
            self.imgDisplayLayout = QtGui.QVBoxLayout()
        else:
            self.imgDisplayLayout = QtGui.QHBoxLayout()

        self.pixmapLabels = []
        imagesInDirectory = ProjectManagers.getImagesInDirectory( directory=self.currentFolderShown )
        for image in imagesInDirectory:
            filePath = os.path.join( self.currentFolderShown, image )

            # Create a label to contain the pixmap
            tmp = QtGui.QLabel(self.imageDisplayAreaContents)
            self.pixmapLabels.append( tmp )
            label_pixmapContainer = self.pixmapLabels[-1]
            label_pixmapContainer.setAlignment(QtCore.Qt.AlignCenter)
            label_pixmapContainer.clear()

            # Adding the image to the label
            pixmap_ImageViewer = QtGui.QPixmap( filePath )
            # label_pixmapContainer.setPixmap( pixmap_ImageViewer.scaled( 650, 650, QtCore.Qt.KeepAspectRatio ) )
            if multipleImageLayoutDirection == "Vertical":
                label_pixmapContainer.setPixmap( pixmap_ImageViewer.scaledToWidth( 700 ) )
            else:
                label_pixmapContainer.setPixmap( pixmap_ImageViewer.scaledToHeight( 500 ) )
            self.imgDisplayLayout.addWidget( label_pixmapContainer )

        # Setting the widget to make the item visible
        self.imageDisplayAreaContents.setLayout( self.imgDisplayLayout )
        self.imgDisplayScrollArea.setWidget( self.imageDisplayAreaContents )


    def updateImageDisplay(self):
        currentImagePath = self.currentImageShownPath
        currentDirectoryPath = os.path.dirname( currentImagePath )
        if not os.path.exists( currentImagePath ):
            if not os.path.exists( currentDirectoryPath ):
                self.currentImageShownPath = None
            else:
                remainingImages = ProjectManagers.getImagesInDirectory( currentDirectoryPath )
                if len( remainingImages ) == 0:
                    self.currentImageShownPath = None
                    self.currentFolderShown = None
                else:
                    self.currentImageShownPath = os.path.join( currentDirectoryPath, remainingImages[0] )
        self.showImage( imagePath=self.currentImageShownPath )

    def addImage( self, type="single", directoryPath=None ):
        if not self.currentProjectPath:
            self.logError( message=Loggers.msgNormal( "A project must be opened before opening an image." ) )
            return

        # getOpenFileName returns the tuple ( file path, wildcard )
        if type == "multiple":
            files = QtGui.QFileDialog.getOpenFileNames( self, "Open Image", dir=self.currentProjectPath)
            files = files[0]
        else:
            files = QtGui.QFileDialog.getOpenFileName( self, "Open Image", dir=self.currentProjectPath )
            if files[0] == "" or files[0] == None:
                files = []
            else:
                files = [ files[0] ]

        if not files:
            self.log( Loggers.msgNormal( "No image(s) selected." ) )
            return

        if not directoryPath:
            directoryPath = os.path.join( self.currentProjectPath, "Images" )

        self.log( message=Loggers.msgNormal( "Trying to open the image" ) )
        for filePath in files:
            if not FileManagers.isValidImageFile( filePath=filePath ):
                self.logError( message=Loggers.msgUnsupportedFiletype( filePath=filePath ) )
                return
            # TODO: Write code to clear image display
            try:
                ProjectManagers.copyImageToProject( srcPath= os.path.dirname(filePath),
                                                    destPath=directoryPath,
                                                    filename=os.path.basename(filePath))
                self.logSuccess( message="Image opened successfully." )
                self.generateDirTree()
            except Exception as e:
                print e
                self.logError( message=Loggers.msgNormal( str(e) ) )
            else:
                self.currentFolderShown = directoryPath
                self.showImage( imagePath=os.path.join(directoryPath, os.path.basename(filePath)) )
        return

    # =================================================================================================================

    # =================================================================================================================
    # Deleting Items

    def deletePath( self, itemPath ):
        if FileManagers.isNonEmptyDir( itemPath ):
            confirmDeletion = QtGui.QMessageBox.question( self, "Confirm Delete",
                                                      "The directory is not empty. Continue with deletion ?",
                                                      QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel )
            if confirmDeletion == QtGui.QMessageBox.Cancel:
                return
        self.removeItemFromDirTree( itemPath )
        ProjectManagers.removeItemFromProject( itemPath )
        self.updateRecentProjects()
        self.updateImageDisplay()

    def clearImageView( self ):
        self.currentImageShownPath = None
        self.currentFolderShown = None
        # Deleting all the items in the display
        for image in self.pixmapLabels[::-1]:
            image.setParent(None)
            self.pixmapLabels.pop()


    def closeProject( self ):
        self.currentProjectPath = None
        self.treeWidget_dirTree.clear()
        self.clearImageView()
        self.setWindowTitle( "WF2HTML" )


    def deleteProject( self ):
        confirmProjectDelete = QtGui.QMessageBox.question( self, "Confirm Project Delete",
                                                           "Are you sure you want to delete the project ? All will be lost.",
                                                           QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel )
        if confirmProjectDelete == QtGui.QMessageBox.Ok:
            projectPath = self.currentProjectPath
            self.closeProject()
            ProjectManagers.deleteProject( projectPath=projectPath )
            self.updateRecentProjects()

    # =================================================================================================================
    # Loggers
    def clearLog( self ):
        self.textarea_LogDisplay.clear()

    def log( self, message ):
        self.textarea_LogDisplay.insertHtml( message + "<br>" )

    @Slot(str)
    def logJs( self, message ):
        self.textarea_LogDisplay.insertHtml( message + "<br>" )

    def logError( self, message ):
        self.log( "<span style='color: red;'>" + message + "</span>" )

    def logSuccess( self, message ):
        self.log( "<span style='color: green;'>" + message + "</span>" )

    # =================================================================================================================
    # Functions called from javascript

    @Slot(str, str)
    def changeHtmlTag(self, selectedId, targetTagType):
        HtmlManager.changeHtmlTag(htmlFilePath=self.splitScreenDialog.currentHtmlPath, id=selectedId, targetTagType=targetTagType)
        self.splitScreenDialog.updateHtmlCode()
        self.splitScreenDialog.refreshWebView()
        self.splitScreenDialog.webFrame.addToJavaScriptWindowObject('WebViewController', self)
        self.splitScreenDialog.show()

    @Slot(str)
    def deleteHtmlElement( self, selectedId ):
        HtmlManager.deleteHtmlElement( htmlFilePath=self.splitScreenDialog.currentHtmlPath, id=selectedId )
        self.splitScreenDialog.updateHtmlCode()
        self.splitScreenDialog.refreshWebView()
        self.splitScreenDialog.webFrame.addToJavaScriptWindowObject('WebViewController', self)
        self.splitScreenDialog.show()


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_designer\mainWindow.ui'
#
# Created: Sat Mar 10 02:24:46 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#


from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        self.widget_Main = QtGui.QWidget(MainWindow)

        self.hBoxLayout = QtGui.QHBoxLayout( self.widget_Main )

        self.treeWidget_dirTree = QtGui.QTreeWidget(self.widget_Main)
        self.treeWidget_dirTree.header().setVisible(False)

        self.label_pixmapContainer = QtGui.QLabel(self.widget_Main)
        self.label_pixmapContainer.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pixmapContainer.setSizePolicy( QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)

        self.textarea_LogDisplay = QtGui.QTextEdit(self.widget_Main)
        self.textarea_LogDisplay.setReadOnly(True)

        self.splitter_H = QtGui.QSplitter( QtCore.Qt.Horizontal)
        self.splitter_H.addWidget( self.treeWidget_dirTree )
        self.splitter_H.addWidget( self.label_pixmapContainer )
        self.splitter_H.setSizes([3000, 10000])

        self.splitter_V = QtGui.QSplitter( QtCore.Qt.Vertical)
        self.splitter_V.addWidget( self.splitter_H )
        self.splitter_V.addWidget( self.textarea_LogDisplay )
        self.splitter_V.setSizes([12000, 2000])

        self.hBoxLayout.addWidget( self.splitter_V )
        self.setLayout( self.hBoxLayout )

        MainWindow.setCentralWidget(self.widget_Main)

        self.menubar = QtGui.QMenuBar(MainWindow)

        MainWindow.setMenuBar(self.menubar)

        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuNew = QtGui.QMenu(self.menuFile)
        self.actionNew_Image = QtGui.QAction(MainWindow)
        self.menuNew.addAction(self.actionNew_Image)

        self.menuOpen_Recent_Project = QtGui.QMenu(self.menuFile)
        self.actionNo_recent_projects = QtGui.QAction(MainWindow)
        self.menuOpen_Recent_Project.addAction(self.actionNo_recent_projects)

        self.actionNew_Project = QtGui.QAction(MainWindow)
        self.actionOpen_Project = QtGui.QAction(MainWindow)
        self.actionSettings = QtGui.QAction(MainWindow)
        self.menuFile.addAction(self.actionNew_Project)
        self.menuFile.addAction(self.actionOpen_Project)
        self.menuFile.addAction(self.menuOpen_Recent_Project.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuNew.menuAction())

        self.menuEdit = QtGui.QMenu(self.menubar)
        self.actionClear_Log = QtGui.QAction(MainWindow)
        self.menuEdit.addAction(self.actionClear_Log)
        self.actionEdit_MsPaint = QtGui.QAction(MainWindow)
        self.menuEdit.addAction(self.actionEdit_MsPaint)
        self.actionRefresh_Image = QtGui.QAction(MainWindow)
        self.menuEdit.addAction(self.actionRefresh_Image)

        self.menuConvert = QtGui.QMenu(self.menubar)
        self.actionConvert_showInDialog = QtGui.QAction(MainWindow)
        self.menuConvert.addAction(self.actionConvert_showInDialog)
        self.actionConvert_showInBrowser = QtGui.QAction(MainWindow)
        self.menuConvert.addAction(self.actionConvert_showInBrowser)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuConvert.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "WF2HTML", None, QtGui.QApplication.UnicodeUTF8))
        self.label_pixmapContainer.setText(QtGui.QApplication.translate("MainWindow", "Create a project ( Ctrl + Shift + N )", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuNew.setTitle(QtGui.QApplication.translate("MainWindow", "New Image", None, QtGui.QApplication.UnicodeUTF8))
        self.menuOpen_Recent_Project.setTitle(QtGui.QApplication.translate("MainWindow", "Open Recent Project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuConvert.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Image.setText(QtGui.QApplication.translate("MainWindow", "New Image", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Image.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConvert_showInDialog.setText(QtGui.QApplication.translate("MainWindow", "Convert & Show in Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConvert_showInBrowser.setText(QtGui.QApplication.translate("MainWindow", "Convert & Show in Browser", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear_Log.setText(QtGui.QApplication.translate("MainWindow", "Clear Log", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit_MsPaint.setText(QtGui.QApplication.translate("MainWindow", "Edit in MS Paint", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRefresh_Image.setText(QtGui.QApplication.translate("MainWindow", "Refresh Image", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Project.setText(QtGui.QApplication.translate("MainWindow", "New Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Project.setToolTip(QtGui.QApplication.translate("MainWindow", "New Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Project.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Project.setText(QtGui.QApplication.translate("MainWindow", "Open Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Project.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setText(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNo_recent_projects.setText(QtGui.QApplication.translate("MainWindow", "No recent projects", None, QtGui.QApplication.UnicodeUTF8))


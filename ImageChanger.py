import os
import sys
import platform
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import helpform
import newimagedlg

import qrc_resources


class MainWindow(QMainWindow):
    def __init__(self,parent = None):
        super(MainWindow, self).__init__(parent)

        self.image = QImage()
        self.dirty = False
        self.filename = None
        self.mirroredvertically = False
        self.mirroredhorizontally = False

        self.imagelabel = QLabel()
        self.imagelabel.setMinimumSize(200,200)
        self.imagelabel.setAlignment(Qt.AlignCenter)
        self.imagelabel.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.imagelabel)

        logDockWidget= QDockWidget("Log",self)
        logDockWidget.setObjectName("LogDockWidget")
        logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.listWidget = QListWidget()
        logDockWidget.setWidget(self.listWidget)
        self.addDockWidget(Qt.RightDockWidgetArea,logDockWidget)

        self.printer = None

        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage("Ready",5000)

        fileNewAction = QAction(QIcon(":/filenew.png"),"&New",self)
        fileNewAction.setShortcut(QKeySequence.New)
        helptext = "Create New Image"
        fileNewAction.setToolTip(helptext)
        fileNewAction.setStatusTip(helptext)
        fileNewAction.triggered.connect(self.new)

        fileMenu.addAction(fileNewAction)
        fileToolbar.addAction(fileNewAction)

    def createAction(self,text,slot=None,shortcut=None,icon=None,tip=None,checkable=False):
        action = QAction(text,self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png"%icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action



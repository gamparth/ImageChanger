import os
import sys
import platform
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import newimagedlg
import resizedlg
import  helpform
import qrc_resources

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.image = QImage()
        self.dirty = False
        self.filename = None
        self.mirroredvertically = False
        self.mirroredhorizontally = False

        self.imagelabel = QLabel()
        self.imagelabel.setMinimumSize(200, 200)
        self.imagelabel.setAlignment(Qt.AlignCenter)
        self.imagelabel.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.imagelabel)

        logDockWidget = QDockWidget("Log", self)
        logDockWidget.setObjectName("LogDockWidget")
        logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.listWidget = QListWidget()
        logDockWidget.setWidget(self.listWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, logDockWidget)

        self.printer = None

        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage("Ready", 5000)

        fileNewAction = self.createAction('&New', QKeySequence.New, "filenew", "Create an image file")
        fileNewAction.triggered.connect(self.fileNew)
        fileOpenAction = self.createAction('&Open',QKeySequence.Open,'fileopen',"Open Image")
        fileOpenAction.triggered.connect(self.fileOpen)
        fileSaveAction = self.createAction("&Save", QKeySequence.Save, "filesave", "Save Image ")
        fileSaveAction.triggered.connect(self.fileSave)
        fileSaveAsAction = self.createAction("Save &As", QKeySequence.SaveAs, "filesaveas", "Save As")
        fileSaveAsAction.triggered.connect(self.fileSaveAs)
        filePrintAction = self.createAction("&Print", QKeySequence.Print, "fileprint", "Print Image")
        # filePrintAction.triggered.connect(self.print)

        fileQuitAction = self.createAction("&Quit", "Ctrl+Q", "filequit", "Close the application")
        fileQuitAction.triggered.connect(self.close)
        editZoomAction = self.createAction("&Zomm", "Alt+Z", "editzoom", "Zoom the image")
        editZoomAction.triggered.connect(self.editZoom)
        editInvertAction = self.createAction("&Invert", "Ctrl+I", "invert", "Invert the image color", True)
        editInvertAction.toggled.connect(self.editInvert)
        editImageResizeAction = self.createAction("&Resize","Ctrl+R")
        editImageResizeAction.triggered.connect(self.editimageresize)

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenuActions = (fileNewAction, fileOpenAction,fileSaveAction, fileSaveAsAction, filePrintAction, fileQuitAction)
        self.fileMenu.aboutToShow.connect(self.updateFileMenu)

        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editInvertAction, editZoomAction,editImageResizeAction))

        QCoreApplication.setAttribute(Qt.AA_DontUseNativeMenuBar)

        mirrorGroup = QActionGroup(self)
        editUnMirrorAction = self.createAction("&Unmirror", "Ctrl+U", "editunmirror", "Unmirror the image", True)
        editUnMirrorAction.triggered.connect(self.editUnMirror)
        editHoriMirrorAction = self.createAction("&Mirror Horizontal", "Ctrl+H", ":/mhorizontal",
                                                 "Mirror Image Horizontaly")
        editHoriMirrorAction.triggered.connect(self.editMirrorHorizontal)
        editVertMirrorAction = self.createAction("&Mirror Vertical", "Ctrl+V", ":/mvertical", "Mirror Image Vertically")
        editVertMirrorAction.triggered.connect(self.editMirrorVertical)
        self.addActions(mirrorGroup, (editUnMirrorAction, editHoriMirrorAction, editVertMirrorAction))
        editUnMirrorAction.setChecked(True)


        mirrormenu = editMenu.addMenu(QIcon(":/editmirror.png"), "&Mirror")

        self.addActions(mirrormenu, (editUnMirrorAction, editHoriMirrorAction, editVertMirrorAction))

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileNewAction,fileOpenAction, fileSaveAction, filePrintAction))

        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(editToolbar, (editZoomAction, editUnMirrorAction, editInvertAction))

        self.zoomspinbox = QSpinBox()
        self.zoomspinbox.setMinimum(-500)
        self.zoomspinbox.setMaximum(500)
        self.zoomspinbox.setSuffix(" %"),
        self.zoomspinbox.setValue(100)
        self.setToolTip("Zoom the image")
        self.setStatusTip(self.zoomspinbox.toolTip())
        self.zoomspinbox.setFocusPolicy(Qt.NoFocus)
        self.zoomspinbox.valueChanged.connect(self.showImage)

        editToolbar.addWidget(self.zoomspinbox)

        self.addActions(self.imagelabel,
                        (editInvertAction, editUnMirrorAction, editVertMirrorAction, editHoriMirrorAction))

        self.resetableActions = ((editUnMirrorAction, True), (editInvertAction, False))

        helpMenu = self.menuBar().addMenu("Help")
        helpAbout = self.createAction("A&bout", QKeySequence.HelpContents, ":/help", "About")
        helpAbout.triggered.connect(self.helpAbout)
        helpMenu.addAction(helpAbout)

        setting = QSettings()
        self.recentFiles = setting.value('RecentFiles.', type=str)
        size = setting.value("MainWindow/Size", QSize(600, 500))
        self.resize(size)
        position = setting.value("MainWindow/Position", QPoint(0, 0))

        self.move(position)
        self.restoreState(setting.value("MainWindow/State", type=QByteArray))
        self.setWindowTitle("Image Changer")
        self.updateFileMenu()
        QTimer.singleShot(0, self.loadInitialFile)

    def createAction(self, text, shortcut=None, icon=None, tip=None, checkable=False):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeperator()
            else:
                target.addAction(action)

    def updateFileMenu(self):
        self.fileMenu.clear()
        self.addActions(self.fileMenu, (self.fileMenuActions[:-1]))
        current = self.filename if self.filename is not None else None
        recentFiles = []
        for fname in self.recentFiles:
            if fname != current and QFile.exists(fname):
                recentFiles.append(fname)
        if recentFiles:
            self.fileMenu.addSeparator()
            for i, fname in enumerate(recentFiles):
                action = QAction(QIcon(":/icon.png"), "&%d %s" % (i + 1, QFileInfo(fname).fileName()), self)
                action.setData(fname)
                action.triggered.connect(self.loadFile)
                self.fileMenu.addAction(action)
            self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.fileMenuActions[-1])

    def loadInitialFile(self):
        settings = QSettings()
        fname = settings.value("LastFile")
        if fname and QFile.exists(fname):
            self.loadFile(fname)

    def closeEvent(self, event):
        if self.okToContinue():
            settings = QSettings()
            filename = QVariant(self.filename) if self.filename is not None else QVariant()
            settings.setValue("LastFile", filename)
            recentFiles = QVariant(self.recentFiles) if self.recentFiles else QVariant()
            settings.setValue("RecentFiles", recentFiles)
            settings.setValue("MainWindow/Size", QVariant(self.size()))
            settings.setValue("MainWindow/Position", QVariant(self.pos()))
            settings.setValue("MainWindows/State", QVariant(self.saveState()))
        else:
            event.ignore()

    def okToContinue(self):
        if self.dirty:
            reply = QMessageBox.question(self, "Image Change -Unsaved Changes", "Save unsaved changes ?",
                                         QMessageBox.Yes \
                                         | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                self.filesave()
        return True

    def addRecentFiles(self, fname):
        if fname is None:
            return
        if fname[0] not in self.recentFiles:
            self.recentFiles = fname[0] + self.recentFiles[:8]

    def fileNew(self):
        if not self.okToContinue():
            return
        dialog = newimagedlg.NewImageDlg(self)
        if dialog.exec_():
            self.addRecentFiles(self.filename)
            self.image = QImage()
            for action, check in self.resetableActions:
                action.setChecked(check)
            self.image = dialog.image()
            self.filename = None
            self.dirty = True
            self.showImage()
            self.sizeLabel.setText("%d x %d" % (self.image.width(), self.image.height()))
            self.updateStatus("Created New Image")

    def updateStatus(self, message):
        self.statusBar().showMessage(message, 5000)
        self.listWidget.addItem(message)
        if self.filename is not None:
            self.setWindowTitle("Image Changer - %s[*]" % os.path.basename(self.filename))
        elif not self.image.isNull():
            self.setWindowTitle("Image Changer - Unamed[*]")
        else:
            self.setWindowTitle("Image Changer[*]")
        self.setWindowModified(self.dirty)

    def fileOpen(self):
        if not self.okToContinue():
            return
        dir = os.path.dirname(self.filename) if self.filename is not None else "."
        formats = ["*.{}".format(format.data().decode("ascii").lower()) for format in QImageReader.supportedImageFormats()]
        fname = QFileDialog.getOpenFileName(self, "Image Change - Choose Image", dir,
                                            "Image files (%s)" % " ".join(formats))
        if fname:
            self.loadFile(fname[0])

    def loadFile(self, fname=None):
        if fname is None:
            action = self.sender()
            if isinstance(action, QAction):
                fname = action.data()
                if not self.okToContinue():
                    return
            else:
                return
        if fname:
            self.filename = None
            image = QImage(fname)
            if image.isNull():
                message = "Failed to  read %s" % fname
            else:
                self.addRecentFiles(fname)
                self.image = QImage()
                for action, check in self.resetableActions:
                    action.setChecked(check)
                self.image = image
                self.filename = fname
                self.showImage()
                self.dirty = False
                self.sizeLabel.setText("%d x %d" % (image.width(), image.height()))
                message = "Loaded %s" % os.path.basename(fname)
            self.updateStatus(message)

    def fileSave(self):
        if self.image.isNull():
            return
        if self.filename is None:
            self.fileSaveAs()
        else:
            if self.image.save(self.filename, None):
                self.updateStatus("Saved  as %s" % self.filename)
                self.dirty = False
            else:
                self.updateStatus("Failed to save %s" % self.filename)

    def fileSaveAs(self):
        if self.image.isNull():
            return
        fname = self.filename if self.filename is not None else "."
        formats = ["*.{}".format(format.data().decode("ascii")).lower() for format in QImageWriter.supportedImageFormats()]
        fname,form = QFileDialog.getSaveFileName(self, "Image Changer - Save File", fname,
                                            "Image files (%s)" % " ".join(formats))
        if fname:
            if "." not in fname:
                fname += ".png"
                self.addRecentFiles(fname)
                self.filename = fname
                self.fileSave()

    def editInvert(self, on):
        if self.image.isNull():
            return
        self.image.invertPixels()
        self.showImage()
        self.dirty = True
        self.updateStatus("Inverted" if on else "Uninverted")

    def editMirrorHorizontal(self, on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(True, False)
        self.showImage()
        self.mirroredhorizontally = not self.mirroredhorizontally
        self.dirty = True
        self.updateStatus("Mirrored Horizonally" if on else "Unmirrored Horizontally")

    def editMirrorVertical(self, on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(False, True)
        self.showImage()
        self.mirroredvertically = not self.mirroredvertically
        self.dirty = True
        self.updateStatus(("Mirrored Vertically" if on else "Unmirrored Vertically"))

    def editUnMirror(self, on):
        if self.image.isNull():
            return
        if self.mirroredvertically:
            self.editMirrorVertical(False)
        if self.mirroredhorizontally:
            self.editMirrorHorizontal(False)

    def editZoom(self):
        if self.image.isNull():
            return
        percent, ok = QInputDialog.getInt(self, "Image Changer - Zoom", "Percent :", self.zoomspinbox.value(), 1, 400)
        if ok:
            self.zoomspinbox.setValue(percent)

    def showImage(self, percent=None):
        if self.image.isNull():
            return
        if percent is None:
            percent = (self.imagelabel.height()/self.image.height())*100 if self.imagelabel.height()/self.image.height() <1 else 100
            self.zoomspinbox.setValue(percent)
        factor = percent / 100.0
        width = self.image.width() *factor
        height = self.image.height()*factor
        image = self.image.scaled(int(width), int(height), Qt.KeepAspectRatio)
        self.imagelabel.setPixmap(QPixmap.fromImage(image))



    def editimageresize(self):
        rd = resizedlg.ResizeDlg(self.imagelabel.width(),self.imagelabel.height())
        if rd.exec_():
            w,h = rd.result()
            self.imagelabel.resize(w,h)

            factor = h / self.image.height()
            per=factor*100
            self.zoomspinbox.setValue(per)


    def helpAbout(self):
        QMessageBox.about(self,"About Image Changer", """<b>Image Changer</b> v %s <p>Copyright &copy; 2017 Ak Ltd. All right
        reserved.
        <p>This application can be used to perform simple image manipulations.
        <p>Python %s - Qt %s - PyQt %s on %s""" % (
        "3.6", platform.python_version(), QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setOrganizationName("Abhi Ltd.")
    app.setOrganizationDomain("xxx.com")
    app.setApplicationName("Image Changer")
    app.setWindowIcon(QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_()




# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mynewdlg.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_ImageChooserDlg(object):
    def setupUi(self, ImageChooserDlg):
        ImageChooserDlg.setObjectName("ImageChooserDlg")
        ImageChooserDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        ImageChooserDlg.resize(370, 239)
        ImageChooserDlg.setMinimumSize(QtCore.QSize(357, 230))
        ImageChooserDlg.setSizeGripEnabled(False)
        ImageChooserDlg.setModal(False)
        self.gridLayout_2 = QtWidgets.QGridLayout(ImageChooserDlg)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(ImageChooserDlg)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.spinBoxWidth = QtWidgets.QSpinBox(ImageChooserDlg)
        self.spinBoxWidth.setMinimumSize(QtCore.QSize(96, 0))
        self.spinBoxWidth.setMaximumSize(QtCore.QSize(96, 16777215))
        self.spinBoxWidth.setObjectName("spinBoxWidth")
        self.gridLayout.addWidget(self.spinBoxWidth, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(ImageChooserDlg)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.spinBoxHeight = QtWidgets.QSpinBox(ImageChooserDlg)
        self.spinBoxHeight.setMinimumSize(QtCore.QSize(96, 0))
        self.spinBoxHeight.setMaximumSize(QtCore.QSize(96, 16777215))
        self.spinBoxHeight.setObjectName("spinBoxHeight")
        self.gridLayout.addWidget(self.spinBoxHeight, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(ImageChooserDlg)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(ImageChooserDlg)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.colorLabel = QtWidgets.QLabel(ImageChooserDlg)
        self.colorLabel.setText("")
        self.colorLabel.setObjectName("colorLabel")
        self.gridLayout.addWidget(self.colorLabel, 3, 1, 1, 1)
        self.colorButton = QtWidgets.QPushButton(ImageChooserDlg)
        self.colorButton.setObjectName("colorButton")
        self.gridLayout.addWidget(self.colorButton, 3, 2, 1, 1)
        self.brushComboBox = QtWidgets.QComboBox(ImageChooserDlg)
        self.brushComboBox.setObjectName("brushComboBox")
        self.gridLayout.addWidget(self.brushComboBox, 2, 1, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(17, 34, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.okButton = QtWidgets.QPushButton(ImageChooserDlg)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(ImageChooserDlg)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.colorLabel.raise_()
        self.colorButton.raise_()
        self.label_4.raise_()
        self.colorButton.raise_()
        self.colorLabel.raise_()
        self.label.setBuddy(self.spinBoxWidth)
        self.label_2.setBuddy(self.spinBoxHeight)
        self.label_3.setBuddy(self.brushComboBox)
        self.label_4.setBuddy(self.colorButton)

        self.retranslateUi(ImageChooserDlg)
        self.okButton.clicked.connect(ImageChooserDlg.accept)
        self.cancelButton.clicked.connect(ImageChooserDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(ImageChooserDlg)
        ImageChooserDlg.setTabOrder(self.spinBoxWidth, self.spinBoxHeight)
        ImageChooserDlg.setTabOrder(self.spinBoxHeight, self.brushComboBox)
        ImageChooserDlg.setTabOrder(self.brushComboBox, self.colorButton)
        ImageChooserDlg.setTabOrder(self.colorButton, self.okButton)
        ImageChooserDlg.setTabOrder(self.okButton, self.cancelButton)

    def retranslateUi(self, ImageChooserDlg):
        _translate = QtCore.QCoreApplication.translate
        ImageChooserDlg.setWindowTitle(_translate("ImageChooserDlg", "Image Chooser - New Image"))
        self.label.setText(_translate("ImageChooserDlg", "&Width:"))
        self.label_2.setText(_translate("ImageChooserDlg", "&Height:"))
        self.label_3.setText(_translate("ImageChooserDlg", "&Brush pattern:"))
        self.label_4.setText(_translate("ImageChooserDlg", "&Color"))
        self.colorButton.setText(_translate("ImageChooserDlg", "Color..."))
        self.okButton.setText(_translate("ImageChooserDlg", "Ok"))
        self.cancelButton.setText(_translate("ImageChooserDlg", "Cancel"))


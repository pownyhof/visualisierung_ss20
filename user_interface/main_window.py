# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 250)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(170, 30, 61, 97))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lte_button = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.lte_button.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lte_button.sizePolicy().hasHeightForWidth())
        self.lte_button.setSizePolicy(sizePolicy)
        self.lte_button.setChecked(True)
        self.lte_button.setObjectName("lte_button")
        self.verticalLayout.addWidget(self.lte_button)
        self.umts_button = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.umts_button.setObjectName("umts_button")
        self.verticalLayout.addWidget(self.umts_button)
        self.gsm_button = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.gsm_button.setObjectName("gsm_button")
        self.verticalLayout.addWidget(self.gsm_button, 0, QtCore.Qt.AlignLeft)
        self.generate_button = QtWidgets.QPushButton(self.centralwidget)
        self.generate_button.setGeometry(QtCore.QRect(150, 140, 100, 50))
        self.generate_button.setObjectName("generate_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lte_button.setText(_translate("MainWindow", "LTE"))
        self.umts_button.setText(_translate("MainWindow", "UMTS"))
        self.gsm_button.setText(_translate("MainWindow", "GSM"))
        self.generate_button.setText(_translate("MainWindow", "Generieren"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'steve.ui'
#
# Created: Mon Jul 18 13:59:25 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(683, 523)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.mosaicGroupBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mosaicGroupBox.sizePolicy().hasHeightForWidth())
        self.mosaicGroupBox.setSizePolicy(sizePolicy)
        self.mosaicGroupBox.setMinimumSize(QtCore.QSize(200, 200))
        self.mosaicGroupBox.setObjectName(_fromUtf8("mosaicGroupBox"))
        self.horizontalLayout.addWidget(self.mosaicGroupBox)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.positionsLabel = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.positionsLabel.sizePolicy().hasHeightForWidth())
        self.positionsLabel.setSizePolicy(sizePolicy)
        self.positionsLabel.setObjectName(_fromUtf8("positionsLabel"))
        self.verticalLayout.addWidget(self.positionsLabel)
        self.positionsFrame = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.positionsFrame.sizePolicy().hasHeightForWidth())
        self.positionsFrame.setSizePolicy(sizePolicy)
        self.positionsFrame.setMinimumSize(QtCore.QSize(150, 0))
        self.positionsFrame.setMaximumSize(QtCore.QSize(150, 16777215))
        self.positionsFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.positionsFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.positionsFrame.setObjectName(_fromUtf8("positionsFrame"))
        self.verticalLayout.addWidget(self.positionsFrame)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.mosaicLabel = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mosaicLabel.sizePolicy().hasHeightForWidth())
        self.mosaicLabel.setSizePolicy(sizePolicy)
        self.mosaicLabel.setObjectName(_fromUtf8("mosaicLabel"))
        self.horizontalLayout_2.addWidget(self.mosaicLabel)
        self.xLabel = QtGui.QLabel(self.centralwidget)
        self.xLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.xLabel.setObjectName(_fromUtf8("xLabel"))
        self.horizontalLayout_2.addWidget(self.xLabel)
        self.xSpinBox = QtGui.QSpinBox(self.centralwidget)
        self.xSpinBox.setMinimum(1)
        self.xSpinBox.setProperty(_fromUtf8("value"), 5)
        self.xSpinBox.setObjectName(_fromUtf8("xSpinBox"))
        self.horizontalLayout_2.addWidget(self.xSpinBox)
        self.yLabel = QtGui.QLabel(self.centralwidget)
        self.yLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.yLabel.setObjectName(_fromUtf8("yLabel"))
        self.horizontalLayout_2.addWidget(self.yLabel)
        self.ySpinBox = QtGui.QSpinBox(self.centralwidget)
        self.ySpinBox.setMinimum(1)
        self.ySpinBox.setProperty(_fromUtf8("value"), 3)
        self.ySpinBox.setObjectName(_fromUtf8("ySpinBox"))
        self.horizontalLayout_2.addWidget(self.ySpinBox)
        self.connectRadioButton = QtGui.QRadioButton(self.centralwidget)
        self.connectRadioButton.setObjectName(_fromUtf8("connectRadioButton"))
        self.horizontalLayout_2.addWidget(self.connectRadioButton)
        self.magComboBox = QtGui.QComboBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.magComboBox.sizePolicy().hasHeightForWidth())
        self.magComboBox.setSizePolicy(sizePolicy)
        self.magComboBox.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.magComboBox.setEditable(False)
        self.magComboBox.setObjectName(_fromUtf8("magComboBox"))
        self.horizontalLayout_2.addWidget(self.magComboBox)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 683, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionConnect = QtGui.QAction(MainWindow)
        self.actionConnect.setObjectName(_fromUtf8("actionConnect"))
        self.actionDisconnect = QtGui.QAction(MainWindow)
        self.actionDisconnect.setObjectName(_fromUtf8("actionDisconnect"))
        self.actionSave_Positions = QtGui.QAction(MainWindow)
        self.actionSave_Positions.setObjectName(_fromUtf8("actionSave_Positions"))
        self.actionSave_Mosaic = QtGui.QAction(MainWindow)
        self.actionSave_Mosaic.setObjectName(_fromUtf8("actionSave_Mosaic"))
        self.actionSet_Working_Directory = QtGui.QAction(MainWindow)
        self.actionSet_Working_Directory.setObjectName(_fromUtf8("actionSet_Working_Directory"))
        self.actionLoad_Mosaic = QtGui.QAction(MainWindow)
        self.actionLoad_Mosaic.setObjectName(_fromUtf8("actionLoad_Mosaic"))
        self.actionClear_Mosaic = QtGui.QAction(MainWindow)
        self.actionClear_Mosaic.setObjectName(_fromUtf8("actionClear_Mosaic"))
        self.actionLoad_Positions = QtGui.QAction(MainWindow)
        self.actionLoad_Positions.setObjectName(_fromUtf8("actionLoad_Positions"))
        self.menuFile.addAction(self.actionConnect)
        self.menuFile.addAction(self.actionDisconnect)
        self.menuFile.addAction(self.actionSet_Working_Directory)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClear_Mosaic)
        self.menuFile.addAction(self.actionLoad_Mosaic)
        self.menuFile.addAction(self.actionLoad_Positions)
        self.menuFile.addAction(self.actionSave_Mosaic)
        self.menuFile.addAction(self.actionSave_Positions)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Steve", None, QtGui.QApplication.UnicodeUTF8))
        self.mosaicGroupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Mosaic", None, QtGui.QApplication.UnicodeUTF8))
        self.positionsLabel.setText(QtGui.QApplication.translate("MainWindow", "Positions:", None, QtGui.QApplication.UnicodeUTF8))
        self.mosaicLabel.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.xLabel.setText(QtGui.QApplication.translate("MainWindow", "# X:", None, QtGui.QApplication.UnicodeUTF8))
        self.yLabel.setText(QtGui.QApplication.translate("MainWindow", "# Y:", None, QtGui.QApplication.UnicodeUTF8))
        self.connectRadioButton.setText(QtGui.QApplication.translate("MainWindow", "Connected", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConnect.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDisconnect.setText(QtGui.QApplication.translate("MainWindow", "Disconnect", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Positions.setText(QtGui.QApplication.translate("MainWindow", "Save Positions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Mosaic.setText(QtGui.QApplication.translate("MainWindow", "Save Mosaic", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSet_Working_Directory.setText(QtGui.QApplication.translate("MainWindow", "Set Working Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_Mosaic.setText(QtGui.QApplication.translate("MainWindow", "Load Mosaic", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear_Mosaic.setText(QtGui.QApplication.translate("MainWindow", "Clear Mosaic", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_Positions.setText(QtGui.QApplication.translate("MainWindow", "Load Positions", None, QtGui.QApplication.UnicodeUTF8))


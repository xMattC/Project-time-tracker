# Form implementation generated from reading ui file '.\main_window.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(575, 478)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setEnabled(True)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 261, 131))
        self.groupBox.setObjectName("groupBox")
        self.label_print_out = QtWidgets.QLabel(parent=self.groupBox)
        self.label_print_out.setGeometry(QtCore.QRect(10, 90, 241, 21))
        self.label_print_out.setStyleSheet("")
        self.label_print_out.setObjectName("label_print_out")
        self.layoutWidget = QtWidgets.QWidget(parent=self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 241, 26))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.comboBox_db_projects = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox_db_projects.setObjectName("comboBox_db_projects")
        self.gridLayout.addWidget(self.comboBox_db_projects, 0, 1, 1, 1)
        self.gridLayout.setColumnStretch(1, 3)
        self.layoutWidget1 = QtWidgets.QWidget(parent=self.groupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 60, 239, 26))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_clock_in = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.button_clock_in.setObjectName("button_clock_in")
        self.horizontalLayout.addWidget(self.button_clock_in)
        self.button_clock_out = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.button_clock_out.setObjectName("button_clock_out")
        self.horizontalLayout.addWidget(self.button_clock_out)
        self.pushButton_add_project = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_add_project.setObjectName("pushButton_add_project")
        self.horizontalLayout.addWidget(self.pushButton_add_project)
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 210, 531, 211))
        self.groupBox_2.setObjectName("groupBox_2")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.groupBox_2)
        self.tableWidget.setGeometry(QtCore.QRect(10, 20, 511, 181))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.groupBox_4 = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(290, 10, 261, 201))
        self.groupBox_4.setObjectName("groupBox_4")
        self.tableWidget_reports = QtWidgets.QTableWidget(parent=self.groupBox_4)
        self.tableWidget_reports.setGeometry(QtCore.QRect(10, 20, 241, 171))
        self.tableWidget_reports.setObjectName("tableWidget_reports")
        self.tableWidget_reports.setColumnCount(0)
        self.tableWidget_reports.setRowCount(0)
        self.button_report = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_report.setGeometry(QtCore.QRect(240, 460, 131, 24))
        self.button_report.setObjectName("button_report")
        self.button_sessions = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_sessions.setGeometry(QtCore.QRect(60, 460, 151, 21))
        self.button_sessions.setObjectName("button_sessions")
        self.button_status = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_status.setGeometry(QtCore.QRect(400, 460, 95, 24))
        self.button_status.setObjectName("button_status")
        self.groupBox_3 = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 140, 261, 71))
        self.groupBox_3.setObjectName("groupBox_3")
        self.widget = QtWidgets.QWidget(parent=self.groupBox_3)
        self.widget.setGeometry(QtCore.QRect(10, 30, 241, 26))
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_display_data = QtWidgets.QLabel(parent=self.widget)
        self.label_display_data.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_display_data.setObjectName("label_display_data")
        self.gridLayout_2.addWidget(self.label_display_data, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 1, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 575, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExport_Data = QtGui.QAction(parent=MainWindow)
        self.actionExport_Data.setObjectName("actionExport_Data")
        self.actionGraphs = QtGui.QAction(parent=MainWindow)
        self.actionGraphs.setObjectName("actionGraphs")
        self.actionEdit_Logs = QtGui.QAction(parent=MainWindow)
        self.actionEdit_Logs.setObjectName("actionEdit_Logs")
        self.menuFile.addAction(self.actionExport_Data)
        self.menuFile.addAction(self.actionGraphs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionEdit_Logs)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Clock-in/out"))
        self.label_print_out.setText(_translate("MainWindow", "label_print_out"))
        self.label_2.setText(_translate("MainWindow", "PROJECT"))
        self.button_clock_in.setText(_translate("MainWindow", "Clock-in"))
        self.button_clock_out.setText(_translate("MainWindow", "Clock-out"))
        self.pushButton_add_project.setText(_translate("MainWindow", "Add Project"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Sessions"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Total Hours"))
        self.button_report.setText(_translate("MainWindow", "Report"))
        self.button_sessions.setText(_translate("MainWindow", "Sessions"))
        self.button_status.setText(_translate("MainWindow", "Status"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Display"))
        self.label_display_data.setText(_translate("MainWindow", "Display-data-period"))
        self.pushButton.setText(_translate("MainWindow", "Data"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionExport_Data.setText(_translate("MainWindow", "Export to CSV"))
        self.actionGraphs.setText(_translate("MainWindow", "Graphs"))
        self.actionEdit_Logs.setText(_translate("MainWindow", "Edit Logs"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

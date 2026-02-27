from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import QSoundEffect
import sys
import json


import ui_resources
from GmList import Ui_MainWindow




class GmList(Ui_MainWindow, QMainWindow):

    from TaskDefine import addTask
    from TaskDefine import removeTask
    from TaskDefine import markTaskAsDone
    from TaskDefine import markTaskAsPending
    from TaskDefine import selectAllTasks
    from TaskDefine import applyFilters
    from TaskDefine import updateDuration
    from TaskDefine import updateSummary
    
    from SaveLoad import saveToDoList
    from SaveLoad import save_tasks_to_file
    from SaveLoad import loadToDoList
    from SaveLoad import load_tasks_from_file
    from SaveLoad import newToDoList

    from NotificationTimer import checkForNotifications
    from NotificationTimer import setEnabledDisabledSoundButton
    from NotificationTimer import setIconSoundButton
    
    from MoveTask import moveDownTask
    from MoveTask import moveUpTask
    from MoveTask import connectDurationSignals

    from SortTable import sortTable
    from SortTable import sortByTime
    from SortTable import reorderTable
    from SortTable import sortByDuration
    
    from AboutProgramDefine import openAboutProgramDialog_Define
    from AboutProgramDefine import closeAboutProgramDialog_Define



    # save todolist before exit
    def closeEvent(self, event):
        # creating message box
        message = QMessageBox(self)
        message.setIcon(QMessageBox.Icon.Question)
        message.setWindowTitle("Save Changes?")
        message.setText("Do you want to save your changes?")

        # creating buttons
        yesButton = message.addButton("Yes", QMessageBox.ButtonRole.AcceptRole)
        noButton = message.addButton("No", QMessageBox.ButtonRole.RejectRole)
        
        # set default button
        message.setDefaultButton(yesButton)

        # show message box
        message.exec()

        # what button is pressed?
        if message.clickedButton() == yesButton:
            self.saveToDoList()
        elif message.clickedButton() == noButton:
            pass
        event.accept()



    def __init__(self  ,  appXX):
        super().__init__()
        self.app = appXX
        
        #create window
        self.show()
        self.setupUi(self)

        # variables
        self.soundValue = "True"
        
        # create notification timer
        self.notificationTimer = QTimer(self)
        self.notificationTimer.timeout.connect(self.checkForNotifications)
        self.notificationTimer.start(60_000)
        self.notified_tasks = set()
        
        # create notification sound
        self.notification_sound = QSoundEffect()
        self.notification_sound.setSource(QUrl.fromLocalFile("Sounds/ring-sound-effect.wav"))
        self.notification_sound.setVolume(0.5)

        # setup table
        self.todolist.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.todolist.setColumnWidth(0, 300)
        self.todolist.setColumnWidth(1, 150)
        self.todolist.setColumnWidth(2, 150)
        self.todolist.setColumnWidth(3, 150)
        self.todolist.setColumnWidth(4, 50)
        # create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        
        # signal/slots
        self.newButton.clicked.connect(self.newToDoList)
        self.loadButton.clicked.connect(self.loadToDoList)
        self.saveButton.clicked.connect(self.saveToDoList)
        self.addButton.clicked.connect(self.addTask)
        self.removeButton.clicked.connect(self.removeTask)
        self.markAsDoneButton.clicked.connect(self.markTaskAsDone)
        self.markAsPendingButton.clicked.connect(self.markTaskAsPending)
        self.selectAllButton.clicked.connect(self.selectAllTasks)
        self.moveUpButton.clicked.connect(self.moveUpTask)
        self.moveDownButton.clicked.connect(self.moveDownTask)
        self.reminderButton.clicked.connect(self.setEnabledDisabledSoundButton)
        self.soundButton.clicked.connect(self.setIconSoundButton)
        self.aboutQtButton.clicked.connect(self.app.aboutQt)
        self.aboutButton.clicked.connect(self.openAboutProgramDialog_Define)
        self.sortComboBox.currentTextChanged.connect(self.sortTable)
        self.priorityFilterComboBox.currentTextChanged.connect(self.applyFilters)
        self.tagFilterComboBox.currentTextChanged.connect(self.applyFilters)
        self.filterComboBox.currentTextChanged.connect(self.applyFilters)
        self.searchLineEdit.textChanged.connect(self.applyFilters)

        
myApp = QApplication([])
ui = GmList(myApp)
ui.show()
sys.exit(myApp.exec())
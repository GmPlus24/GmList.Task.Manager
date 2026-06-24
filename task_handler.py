from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import QSoundEffect
import sys
import json
from functools import partial



def addTask(self, row_index):
    # add new ROW
    current_row_count = self.todolist.rowCount()
    self.todolist.insertRow(current_row_count)


    # add new item
    newItem = QTableWidgetItem("")
    newItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter) # align center
    self.todolist.setItem(current_row_count, 0, newItem)


    # add time edit widget to column1
    startTimeEdit = QTimeEdit()
    startTimeEdit.setDisplayFormat("HH:mm")
    startTimeEdit.setTime(QTime.currentTime())
    startTimeEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
    startTimeEdit.timeChanged.connect(self.updateDuration) # for duration
    self.todolist.setCellWidget(current_row_count, 1, startTimeEdit)


    # add time edit widget to column2
    endTimeEdit = QTimeEdit()
    endTimeEdit.setDisplayFormat("HH:mm")
    endTimeEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
    endTimeEdit.setTime(QTime.currentTime().addSecs(1800))
    endTimeEdit.timeChanged.connect(self.updateDuration) # for duration
    self.todolist.setCellWidget(current_row_count, 2, endTimeEdit)

    # set duration 0:30
    item = QTableWidgetItem("0:30")
    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    self.todolist.setItem(current_row_count, 3, item)
    

    # add check box widget to column4
    valueCheckBox = QCheckBox()
    valueCheckBox.stateChanged.connect(self.updateSummary)
    valueCheckBox.stateChanged.connect(self.applyFilters)

    container = QWidget()
    valueLayout = QHBoxLayout(container)
    valueLayout.addWidget(valueCheckBox)
    valueLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    valueLayout.setContentsMargins(0, 0, 0, 0)
    self.todolist.setCellWidget(current_row_count, 4, container)


    # add combobox for tag in column5
    tagComboBox = QComboBox()
    tagComboBox.currentTextChanged.connect(self.applyFilters)
    tagComboBox.addItems(["None", "Work", "Personal", "Important", "Urgent", "University", "Shopping", "Exercise", "Project", "Meeting"])
    self.todolist.setCellWidget(current_row_count, 5, tagComboBox)


    # add checkbox for priority in column 6
    priorityComboBox = QComboBox()
    priorityComboBox.currentTextChanged.connect(self.applyFilters)
    priorityComboBox.addItems(["Low", "Medium", "High"])
    priorityComboBox.setCurrentIndex(1) # set combobox to medium
    self.todolist.setCellWidget(current_row_count, 6, priorityComboBox)


    # set Read-Only column 3
    item = self.todolist.item(current_row_count, 3)
    if item is None:
        item = QTableWidgetItem()
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.todolist.setItem(current_row_count, 3, item)

    # update summary
    self.updateSummary()

    # apply filters
    self.applyFilters()

    # sort table
    self.sortTable()




def removeTask(self):
    selected_rows = set()
    for item in self.todolist.selectedItems():
        selected_rows.add(item.row())

    for row in sorted(selected_rows, reverse=True):
        self.todolist.removeRow(row)

    # update summary
    self.updateSummary()

    # apply filters
    self.applyFilters()

    # sort table
    self.sortTable()




def markTaskAsDone(self):
    selected_rows = set(item.row() for item in self.todolist.selectedItems())

    for row in selected_rows:
        container = self.todolist.cellWidget(row, 4)
        if container:
            checkbox = container.findChild(QCheckBox)
            checkbox.setChecked(True)

    # apply filters
    self.applyFilters()




def markTaskAsPending(self):
    selected_rows = set(item.row() for item in self.todolist.selectedItems())

    for row in selected_rows:
        container = self.todolist.cellWidget(row, 4)
        if container:
            checkbox = container.findChild(QCheckBox)
            checkbox.setChecked(False)

    # apply filters
    self.applyFilters()




def selectAllTasks(self):
    self.todolist.selectAll()




def applyFilters(self, text=""):
    print(">>> Applying Filters")
    filter_priority = self.priorityFilterComboBox.currentText()
    filter_tag = self.tagFilterComboBox.currentText()
    filter_option = self.filterComboBox.currentText()
    search_text = self.searchLineEdit.text().lower()


    for row in range(self.todolist.rowCount()):
        item = self.todolist.item(row, 0)  # title column
        checkbox_container = self.todolist.cellWidget(row, 4)
        checkbox = checkbox_container.findChild(QCheckBox) if checkbox_container else None
        tag = self.todolist.cellWidget(row, 5)
        priority = self.todolist.cellWidget(row, 6)

        match_priority = True
        match_tag = True
        match_search = True
        match_filter = True
        
        if item and search_text:
            match_search = search_text in item.text().lower()

        if checkbox:
            if filter_option == "Only Completed":
                match_filter = checkbox.isChecked()
            elif filter_option == "Only Pending":
                match_filter = not checkbox.isChecked()

        if tag and filter_tag != "All":
            match_tag = tag.currentText() == filter_tag

        if priority and filter_priority != "All":
            match_priority = priority.currentText() == filter_priority



        self.todolist.setRowHidden(row, not (match_search and match_filter and match_tag and match_priority))





def updateDuration(self):
    print(">>> Updating Duration")
    
    sender_widget = self.sender()

    for row in range(self.todolist.rowCount()):
        start_widget = self.todolist.cellWidget(row, 1)
        end_widget = self.todolist.cellWidget(row, 2)


        if start_widget is None or end_widget is None:
            continue


        if sender_widget in (start_widget, end_widget):
            start_time = start_widget.time()
            end_time = end_widget.time()

            # convert to minutes
            start_minutes = start_time.hour() * 60 + start_time.minute()
            end_minutes = end_time.hour() * 60 + end_time.minute()

            duration = end_minutes - start_minutes

            # if it was minus(-)
            if duration < 0:
                duration += 24*60

            my_duration_hours = duration // 60
            my_duration_minutes = duration % 60

            duration_text = f"{my_duration_hours}:{my_duration_minutes:02d}"
            item = self.todolist.item(row, 3)
            if item is None:
                item = QTableWidgetItem()
                self.todolist.setItem(row, 3, item)

            item.setText(duration_text)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            



def updateSummary(self):
    total = self.todolist.rowCount()
    completed = 0

    for row in range(total):
        checkbox_container = self.todolist.cellWidget(row, 4)
        checkbox = checkbox_container.findChild(QCheckBox) if checkbox_container else None
        if checkbox and checkbox.isChecked():
            completed += 1

    pending = total - completed

    message = f"✅ Completed: {completed}  /  🕒 Pending: {pending}  /  📋 Total: {total}"
    self.statusBar.showMessage(message)
    

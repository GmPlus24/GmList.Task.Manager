from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import QSoundEffect
from functools import partial
import sys
import json
import os



def newToDoList(self):
    # creating message box
    message = QMessageBox(self)
    message.setIcon(QMessageBox.Icon.Question)
    message.setWindowTitle("Save Changes?")
    message.setText("Do you want to save your changes?")

    # creating buttons
    yesButton = message.addButton("Yes", QMessageBox.ButtonRole.AcceptRole)
    noButton = message.addButton("No", QMessageBox.ButtonRole.RejectRole)
    cancelButton = message.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)

    # set default button
    message.setDefaultButton(yesButton)

    # show message box
    message.exec()

    # what button is pressed?
    if message.clickedButton() == yesButton:
        self.saveToDoList()
        self.todolist.setRowCount(0) # clear the table
    elif message.clickedButton() == noButton:
        self.todolist.setRowCount(0) # clear the table
    else:
        pass
        
    
    self.updateSummary() # update summary
        


def saveToDoList(self):
    self.save_tasks_to_file()

def save_tasks_to_file(self):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file, _ = QFileDialog.getSaveFileName(self, "Save ToDo List", desktop_path, "JSON Files (*.json);;All Files (*)")

    if file:
        print(f"Saving file to: {file}")
        data = []
        for row in range(self.todolist.rowCount()):
            title_item = self.todolist.item(row, 0)
            start_widget = self.todolist.cellWidget(row, 1)
            end_widget = self.todolist.cellWidget(row, 2)
            checkbox_container = self.todolist.cellWidget(row, 4)
            tag_widget = self.todolist.cellWidget(row, 5)
            priority_widget = self.todolist.cellWidget(row, 6)

            checkbox = checkbox_container.findChild(QCheckBox) if checkbox_container else None

            task = {
                "title": title_item.text() if title_item else "",
                "start": start_widget.time().toString("HH:mm") if start_widget else "00:00",
                "end": end_widget.time().toString("HH:mm") if end_widget else "00:00",
                "done": checkbox.isChecked() if checkbox else False,
                "tag": tag_widget.currentText() if tag_widget else "None",
                "priority": priority_widget.currentText() if priority_widget else "Medium"
            }

            data.append(task)
        try:
            with open(file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(">>> JSON file saved successfully")
        except Exception as e:
            print(">>> Saving JSON file faild", str(e))






def loadToDoList(self):
    self.load_tasks_from_file()
    self.updateSummary()
    self.applyFilters()
    self.sortComboBox.setCurrentText("Custom Order") # set sort combobox to NONE

def load_tasks_from_file(self):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file, _ = QFileDialog.getOpenFileName(self, "Open ToDo List", desktop_path, "JSON Files (*.json);;All Files (*)")


    if file:
        print(f"Loading file from: {file}")

        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("ToDoList.json not found")
            return
        except Exception as e:
            print("Error in loading: ", str(e))
            return
    
        # delete current table
        self.todolist.setRowCount(0)
    
        for task in data:
            row = self.todolist.rowCount()
            self.todolist.insertRow(row)
    
            # column 0: title
            newItem = QTableWidgetItem(task["title"])
            newItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.todolist.setItem(row, 0, newItem)
    
            # column 1: start time
            startTimeEdit = QTimeEdit()
            startTimeEdit.setDisplayFormat("HH:mm")
            startTimeEdit.setTime(QTime.fromString(task["start"], "HH:mm"))
            startTimeEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
            startTimeEdit.timeChanged.connect(self.updateDuration)
            self.todolist.setCellWidget(row, 1, startTimeEdit)
    
            # column 2: end time
            endTimeEdit = QTimeEdit()
            endTimeEdit.setDisplayFormat("HH:mm")
            endTimeEdit.setTime(QTime.fromString(task["end"], "HH:mm"))
            endTimeEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
            endTimeEdit.timeChanged.connect(self.updateDuration)
            self.todolist.setCellWidget(row, 2, endTimeEdit)
    
    
            # column 3: duration
            item = QTableWidgetItem("00")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.todolist.setItem(row, 3, item)
            
            
            
            # UPDATING DURATION ------------------------------------------
            start_time = startTimeEdit.time()
            end_time = endTimeEdit.time()

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
            # UPDATING DURATION ------------------------------------------
            
            
            
            
            
            
            # column 4: checkbox
            valueCheckbox = QCheckBox()
            valueCheckbox.stateChanged.connect(self.updateSummary)
            valueCheckbox.stateChanged.connect(self.applyFilters)

            valueCheckbox.setChecked(task["done"])
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.addWidget(valueCheckbox)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            container.setLayout(layout)
            self.todolist.setCellWidget(row, 4, container)

            # column 5: combobox
            tagComboBox = QComboBox()
            tagComboBox.currentTextChanged.connect(self.applyFilters)
            tagComboBox.addItems(["None", "Work", "Personal", "Important", "Urgent", "University", "Shopping", "Exercise", "Project", "Meeting"])
            tagComboBox.setCurrentText(task["tag"])
            self.todolist.setCellWidget(row, 5, tagComboBox)

            # column 6: combobox
            priorityComboBox = QComboBox()
            priorityComboBox.currentTextChanged.connect(self.applyFilters)
            priorityComboBox.addItems(["Low", "Medium", "High"])
            priorityComboBox.setCurrentText(task["priority"])
            self.todolist.setCellWidget(row, 6, priorityComboBox)




    print(">>> List Loaded Successfully")
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import QSoundEffect
from functools import partial
import sys
import json
import os




def sortTable(self):
    index = self.sortComboBox.currentIndex()

    if index == 0: # Default
        return
    if index == 1:  # A → Z
        self.todolist.sortItems(0, Qt.SortOrder.AscendingOrder)
    elif index == 2:  # Z → A
        self.todolist.sortItems(0, Qt.SortOrder.DescendingOrder)
    elif index == 3:  # Earliest → Latest
        self.sortByTime(column=1, ascending=True)
    elif index == 4:  # Latest → Earliest
        self.sortByTime(column=1, ascending=False)
    elif index == 5:  # Shortest Duration → Longest Duration
        self.sortByDuration(ascending=True)
    elif index == 6:  # Longest Duration → Shortest Duration
        self.sortByDuration(ascending=False)




def sortByTime(self, column, ascending=True):
    row_count = self.todolist.rowCount()

    
    time_data = []
    for row in range(row_count):
        time_edit = self.todolist.cellWidget(row, column)
        if time_edit:
            time = time_edit.time()
            time_data.append((row, time))

    
    time_data.sort(key=lambda x: x[1], reverse=not ascending)
    
    sorted_rows = [row for row, _ in time_data]

    self.reorderTable(sorted_rows)




def sortByDuration(self, ascending=True):
    row_count = self.todolist.rowCount()

    duration_data = []
    for row in range(row_count):
        item = self.todolist.item(row, 3)
        if item:
            time_str = item.text()
            
            try:
                hh, mm = map(int, time_str.split(":"))
                total_minutes = hh * 60 + mm
            except:
                total_minutes = 0
            duration_data.append((row, total_minutes))


    duration_data.sort(key=lambda x: x[1], reverse=not ascending)

    sorted_rows = [row for row, _ in duration_data]

    self.reorderTable(sorted_rows)




def reorderTable(self, sorted_row_indices):
    row_count = self.todolist.rowCount()
    column_count = self.todolist.columnCount()

    rows_data = []
    for var_row in sorted_row_indices:
        row_data = []
        for col in range(column_count):
            item = self.todolist.item(var_row, col)
            widget = self.todolist.cellWidget(var_row, col)

            # QTableWidgetItem (Title, Duration)
            if item:
                new_item = QTableWidgetItem(item.text())
                new_item.setTextAlignment(item.textAlignment())
                row_data.append(new_item)



            # Widgets
            elif widget:
                # QComboBox
                if isinstance(widget, QComboBox):
                    new_widget = QComboBox()
                    for i in range(widget.count()):
                        new_widget.addItem(widget.itemText(i))
                    new_widget.setCurrentIndex(widget.currentIndex())
                    new_widget.currentTextChanged.connect(self.applyFilters)
                    row_data.append(new_widget)

                # QTimeEdit
                elif isinstance(widget, QTimeEdit):
                    new_widget = QTimeEdit()
                    new_widget.setTime(widget.time())
                    new_widget.setDisplayFormat("HH:mm")
                    new_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    row_data.append(new_widget)

                # QWidget
                elif isinstance(widget, QWidget):
                    checkbox = widget.findChild(QCheckBox)
                    if checkbox:
                        new_checkbox = QCheckBox()
                        new_checkbox.setChecked(checkbox.isChecked())
                        new_checkbox.stateChanged.connect(self.updateSummary)
                        new_checkbox.stateChanged.connect(self.applyFilters)

                        new_container = QWidget()
                        new_layout = QHBoxLayout(new_container)
                        new_layout.addWidget(new_checkbox)
                        new_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        new_layout.setContentsMargins(0, 0, 0, 0)

                        row_data.append(new_container)



                else:
                    row_data.append(None)
            else:
                row_data.append(None)
        rows_data.append(row_data)

    # delete current table
    self.todolist.setRowCount(0)

    # add rows and fill table
    for row_data in rows_data:
        row = self.todolist.rowCount()
        self.todolist.insertRow(row)

        for col, data in enumerate(row_data):

            if isinstance(data, QWidget):
                self.todolist.setCellWidget(row, col, data)
            if isinstance(data, QTimeEdit):
                try:
                    data.timeChanged.disconnect()
                except TypeError:
                    pass
                data.timeChanged.connect(self.updateDuration)

            elif isinstance(data, QTableWidgetItem):
                self.todolist.setItem(row, col, data)
            

    # apply filters
    self.applyFilters()

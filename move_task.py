from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import QSoundEffect
import sys
from functools import partial




def moveUpTask(self):
    selected = self.todolist.selectedIndexes()
    if selected:
        # create a set of *unique* rows
        rows = set(i.row() for i in selected)
    else:
        rows = [self.todolist.rowCount() - 1]

    rows_list = list(rows)
    rows_list.sort()  # sort in-place


    if (rows_list[0] > 0):
        for row in sorted(rows_list):
            if row > 0:
                self.todolist.insertRow(row - 1)
                for column in range(self.todolist.columnCount()):
                    self.todolist.setItem(row - 1, column, self.todolist.takeItem(row + 1, column))
                    self.todolist.setCellWidget(row - 1, column, self.todolist.cellWidget(row + 1, column))

                # delete row
                self.todolist.removeRow(row + 1)


    # temporarily set MultiSelection
    table_selection_mode = self.todolist.selectionMode()
    self.todolist.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

    if (rows_list[0] > 0):
        for row in sorted(rows_list):
            self.todolist.selectRow(row - 1)

    # temporarily set MultiSelection
    self.todolist.setSelectionMode(table_selection_mode)


    # update duration
    for row in rows:
        self.connectDurationSignals(row)
        self.connectDurationSignals(row - 1)

    # set sort combobox to NONE
    self.sortComboBox.setCurrentText("Custom Order")





def moveDownTask(self):
    selected = self.todolist.selectedIndexes()

    if selected:
        # create a set of *unique* rows
        rows = set(i.row() for i in selected)
    else:
        rows = [self.todolist.rowCount() - 1]

    rows_list = list(rows)
    rows_list.sort()  # sort in-place

    lastRow = self.todolist.rowCount()
    lastMemberPos = len(rows_list)
    lastSelected = rows_list[lastMemberPos - 1]


    if (lastSelected + 1 < lastRow):
        for row in sorted(rows_list, reverse=True):
            if row < self.todolist.rowCount() - 1:
                self.todolist.insertRow(row + 2)
                for i in range(self.todolist.columnCount()):
                    self.todolist.setItem(row + 2, i, self.todolist.takeItem(row, i))
                    self.todolist.setCellWidget(row + 2, i, self.todolist.cellWidget(row, i))



                # delete row
                self.todolist.removeRow(row)



    # temporarily set MultiSelection
    table_selection_mode = self.todolist.selectionMode()
    self.todolist.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

    if (lastSelected + 1 < lastRow):
        for row in sorted(rows_list, reverse=True):
            self.todolist.selectRow(row + 1)


    # temporarily set MultiSelection
    self.todolist.setSelectionMode(table_selection_mode)


    # update duration
    for row in rows:
        self.connectDurationSignals(row)
        self.connectDurationSignals(row + 1)

    # set sort combobox to NONE
    self.sortComboBox.setCurrentText("Custom Order")

    



def connectDurationSignals(self, row):
    startTimeEdit = self.todolist.cellWidget(row, 1)
    endTimeEdit = self.todolist.cellWidget(row, 2)

    if startTimeEdit and endTimeEdit:
        try:
            startTimeEdit.timeChanged.disconnect()
        except:
            pass
        try:
            endTimeEdit.timeChanged.disconnect()
        except:
            pass

        startTimeEdit.timeChanged.connect(self.updateDuration)
        endTimeEdit.timeChanged.connect(self.updateDuration)
        
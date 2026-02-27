from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import QSoundEffect
import sys
import json


def checkForNotifications(self):
    print(">>> Checking notifications at", QTime.currentTime().toString("HH:mm:ss"))
    
    current_time = QTime.currentTime()
    messages = []

    if self.reminderButton.isChecked():
        for row in range(self.todolist.rowCount()):
            title_item = self.todolist.item(row, 0)
            start_widget = self.todolist.cellWidget(row, 1)
    
            if title_item and isinstance(start_widget, QTimeEdit):
                task_title = title_item.text()
                start_time = start_widget.time()
                
                # ID for task
                task_id = f"{task_title}_{start_time.toString('HH:mm')}"
                
                if task_id in self.notified_tasks:
                    continue
                
                diff = current_time.secsTo(start_time)
                
                if diff < 0:
                    diff += 24 * 3600
                
                minutes_diff = diff // 60
    
                if 0 <= minutes_diff <= 5:
                    self.notified_tasks.add(task_id)
                    messages.append(f"• {task_title} at {start_time.toString('HH:mm')}")
                    
        if messages:
            # play sound
            if self.soundValue == "True":
                self.notification_sound.play()
            else:
                pass

            msg = "\n".join(messages)
            QMessageBox.information(
                self,
                "Upcoming Tasks",
                f"The following tasks are about to start:\n\n{msg}"
            )

    else:
        pass
        



def setEnabledDisabledSoundButton(self):
    if self.reminderButton.isChecked():
        self.soundButton.setEnabled(True)

    elif not self.reminderButton.isChecked():
        self.soundButton.setEnabled(False)

    

def setIconSoundButton(self):
    if self.soundValue == "True":
        self.soundButton.setIcon(QIcon(":/mute-icon"))
        self.soundValue = "False"
    
    else:
        self.soundButton.setIcon(QIcon(":/unmute-icon"))
        self.soundValue = "True"

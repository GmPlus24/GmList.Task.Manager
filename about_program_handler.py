from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import QSoundEffect
import sys
import time



# import the Ui file
import about_program_dialog




def openAboutProgramDialog_Handler(self):
    #window = uic.loadUi("about_program_dialog.ui")
    #window.exec()
    
    self.aboutProgram_Dialog = QDialog()
    self.aboutProgramDialog_Ui = about_program_dialog.Ui_Dialog()
    self.aboutProgramDialog_Ui.setupUi(self.aboutProgram_Dialog)
    
    self.aboutProgramDialog_Ui.OKButton.clicked.connect(self.closeAboutProgramDialog_Handler)  # OKButton pressed >>> close dialog
    
    self.aboutProgram_Dialog.exec()
    
    
    pass
    
    


def closeAboutProgramDialog_Handler(self):
    self.aboutProgram_Dialog.close()

    pass


    
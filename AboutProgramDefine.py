from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import QSoundEffect
import sys
import time



# import the Ui file
import AboutProgramDialog




def openAboutProgramDialog_Define(self):
    #window = uic.loadUi("AboutProgramDialog.ui")
    #window.exec()
    
    self.aboutProgram_Dialog = QDialog()
    self.aboutProgramDialog_Ui = AboutProgramDialog.Ui_Dialog()
    self.aboutProgramDialog_Ui.setupUi(self.aboutProgram_Dialog)
    
    self.aboutProgramDialog_Ui.OKButton.clicked.connect(self.closeAboutProgramDialog_Define)  # OKButton pressed >>> close dialog
    
    self.aboutProgram_Dialog.exec()
    
    
    pass
    
    


def closeAboutProgramDialog_Define(self):
    self.aboutProgram_Dialog.close()

    pass


    
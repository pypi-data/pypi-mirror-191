
from PyQt5 import QtCore, QtGui, QtWidgets
import QT.gui
import sys
import dice

our_dice = dice.Dice()

print(our_dice.r("1d20", 1))

app = QtWidgets.QApplication(sys.argv)
gui_base = QtWidgets.QMainWindow()
ui = QT.gui.Ui_gui_base()
ui.setupUi(gui_base)
gui_base.show()
sys.exit(app.exec_())

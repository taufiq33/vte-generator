from window import *
import sys

appInstance = QApplication(sys.argv)
appWindow = mainWindowApp()

appWindow.show()
appInstance.exec_()

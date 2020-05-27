import logging
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from config import Config
from user_interface.main_dialog import Dialog

logging.basicConfig(format=Config.log_format, level=Config.log_level, datefmt=Config.log_date_format)
logging.info("Application started")

app = QApplication(sys.argv)
dialog = QMainWindow()
ui = Dialog(dialog)
dialog.show()
sys.exit(app.exec_())

##

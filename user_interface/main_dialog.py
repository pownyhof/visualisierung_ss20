"""
This class is the UI. It extends the Ui_MainWindow in design.py that is created with the
QT Designer. The design logic is here
"""
import logging
import os
import webbrowser

from config import Config
from map import Map
from user_interface.main_window import Ui_MainWindow


class Dialog(Ui_MainWindow):

    # initialise all variables and lists for the class
    def __init__(self, parent):
        self.setupUi(parent)
        self.lte_button.setChecked(True)
        self.generate_button.clicked.connect(self.generate_map)
        logging.info('Initialized main dialog')

    def generate_map(self):
        logging.info('Map will be generated')

        # identify checked box
        if self.lte_button.isChecked():
            mobile_network_type = Config.lte
        elif self.umts_button.isChecked():
            mobile_network_type = Config.umts
        elif self.gsm_button.isChecked():
            mobile_network_type = Config.gsm
        else:
            mobile_network_type = Config.lte
            logging.error('No Button checked. Continue with LTE')
        logging.debug('Selected mobile network type: ' + mobile_network_type)

        # get date
        if self.useDate.isChecked():
            use_date = 'true'
        else:
            use_date = 'false'
        start_date = self.startDate.date()
        end_date = self.endDate.date()
        logging.info('should date filter be used: ' + use_date)
        logging.info(start_date)
        logging.info(end_date)

        date = self.dateTimeEdit.dateTime()
        logging.info(date)

        # get time
        if self.useTime.isChecked():
            use_time = 'true'
        else:
            use_time = 'false'
        start_time = self.startTime.time()
        end_time = self.endTime.time()
        logging.info('should time filter be used: ' + use_time)
        logging.info(start_time)
        logging.info(end_time)

        # identify mobile network box
        if self.telekom_button.isChecked():
            network = Config.telekom
        elif self.vodafone_button.isChecked():
            network = Config.vodafone
        elif self.telefonica_button.isChecked():
            network = Config.telefonica
        else:
            network = Config.allNetworks
            logging.error('No Button checked. Continue with all networks')
        logging.debug('Selected network: ' + network)

        # initialize map generator
        map_generator = Map(mobile_network_type, network, use_date, start_date, end_date, use_time, start_time,
                            end_time)
        map_generator.generate_map()
        logging.debug('File path: file://' + os.path.realpath(map_generator.file_path))
        webbrowser.open('file://' + os.path.realpath(map_generator.file_path))

     #, use_date, start_date, end_date, use_time, start_time, end_time
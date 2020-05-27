import logging

import pymongo
from sshtunnel import SSHTunnelForwarder

from config import Config

"""
This class creates a connection to the mongodb and fires the queries or aggregations 
to get the data.
"""


class Connector(object):

    def __init__(self):
        self.key_path = Config.key
        self.server = SSHTunnelForwarder(
            (Config.host, Config.port),
            ssh_username=Config.user,
            ssh_pkey=self.key_path,
            remote_bind_address=(Config.remote_address, Config.remote_port)
        )
        self.conn = None
        self.db = None

    # Connect to the Mongodb server
    def connect(self):
        self.server.start()
        self.conn = pymongo.MongoClient('127.0.0.1', self.server.local_bind_port)
        self.db = self.conn[Config.reduced_cell_id_db]
        logging.info("Connected to mongoDB")

    # Ends the connection to the server
    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
        self.server.stop()

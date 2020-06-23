import logging
import os
import pprint
from pathlib import Path

import folium
from folium.plugins import LocateControl, HeatMap

from color_helper import ColorHelper
from config import Config
from database.connector import Connector


class Map(object):


    def __init__(self, mobile_network_type, network):
        self.mobile_network_type = mobile_network_type
        self.network = network
        self.restructure_col = None
        self.clean_col = None
        self.folder_path = os.path.abspath('maps')
        self.file_path = os.path.join(self.folder_path, 'map_' + self.mobile_network_type.lower() + '.html')

    def generate_map(self):
        # connect to local database
        # client = pymongo.MongoClient('mongodb://localhost:27017/')
        # db = client['test']

        # connect to server
        client = Connector()
        client.connect()
        db = client.db

        def connect_to_collections():
            if self.mobile_network_type == Config.lte:
                collection_name = Config.restructure_lte_col
            elif self.mobile_network_type == Config.umts:
                collection_name = Config.restructure_umts_col
            elif self.mobile_network_type == Config.gsm:
                collection_name = Config.restructure_gsm_col
            else:
                collection_name = Config.restructure_lte_col
                logging.error('No valid mobile_network_type. Continue with default LTE data')

            self.restructure_col = db[collection_name]
            self.clean_col = db[Config.clean_col]
            logging.info(
                'Set mobile network type to {0}. Connected to {1}'.format(self.mobile_network_type, collection_name))

        # set collections (default: lte)
        connect_to_collections()

        map_list = []
        # save squares in a list
        for x in self.restructure_col.find({},
                                           {'latitude': 1, 'longitude': 1, 'square_data': 1, 'cell_tower.mnc': 1}):
           if (x['cell_tower'][0]['mnc']) == int(self.network) or self.network == '0':
                map_list.append({'latitude': x['latitude'],
                                'longitude': x['longitude'],
                                'square_data': x['square_data'],
                                 'mnc': x['cell_tower'][0]['mnc']})

        logging.info('Saved squares in list: ' + str(len(map_list)))
        logging.debug('First entry of map_list:' + pprint.pformat(map_list[0]))

        heatmap_list = []
        # save all locations in a list
        for x in self.clean_col.find({'cell_info.type': self.mobile_network_type},
                                     {'_id': 0, 'location_information.latitude': 1,
                                      'location_information.longitude': 1}):
            entry = [x['location_information']['latitude'], x['location_information']['longitude'], 0.1]
            heatmap_list.append(entry)
        logging.info('Saved locations in list for heatmap: ' + str(len(heatmap_list)))
        logging.debug('First entry of heatmap_list:' + pprint.pformat(heatmap_list[0]))

        # generate the map and add different options
        m = folium.Map(location=Config.default_location, zoom_start=15, tiles='CartoDB positron', control_scale=True,
                       prefer_canvas=True)
        folium.raster_layers.TileLayer(Config.tile_stamen_watercolor, name=Config.tile_stamen_watercolor).add_to(m)
        folium.raster_layers.TileLayer(Config.tile_open_street_map, name=Config.tile_open_street_map).add_to(m)
        folium.raster_layers.TileLayer(Config.tile_stamen_toner, name=Config.tile_stamen_toner).add_to(m)
        folium.raster_layers.TileLayer(Config.tile_carto_db_dark, name=Config.tile_carto_db_dark).add_to(m)
        folium.plugins.Fullscreen().add_to(m)
        logging.info('Initialized map')

        # generate heatmap
        HeatMap(heatmap_list, name='Heatmap', radius=15, show=False).add_to(m)
        logging.info('Generated heatmap')

        # this has to be added after adding all options and the heatmap
        folium.LayerControl().add_to(m)

        color_helper = ColorHelper(self.mobile_network_type)
        # adds all squares to the map
        for x in map_list:
            dbm_mean = 0
            for y in x['square_data']:
                dbm_mean += y['dbm']
            dbm_mean = int(dbm_mean / (len(x['square_data'])))
            color = color_helper.get_color(dbm_mean)
            folium.vector_layers.Rectangle(
                bounds=[[x['latitude'] + 0.00009999, x['longitude'] + 0.00009999],
                        [x['latitude'] + 0.00000000, x['longitude'] + 0.00000000]],
                # popup costs performance. disabled as long as the information is not important
                # popup=x['square_data'],
                tooltip=dbm_mean,
                fill_color=color,
                fill_opacity=0.5,
                stroke=True,
                color=color,
                opacity=0.3,
                weight=1
            ).add_to(m)

        logging.info('Added squares to map')

        # https://stackabuse.com/creating-and-deleting-directories-with-python/
        try:
            Path(self.folder_path).mkdir(exist_ok=True)
        except OSError:
            logging.error('Creation of the directory {0} failed'.format(self.folder_path))
        else:
            logging.info('Successfully created the directory {0}'.format(self.folder_path))
        m.save(self.file_path)
        logging.info('Generated map: ' + self.file_path)

        # disconnect from server
        if type(client) == Connector:
            client.disconnect()
            logging.info('Disconnected from mongoDB')

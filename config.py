"""
This class stores default values, which are the same for the complete program
"""
import logging


class Config(object):
    # database connection data
    key = 'database/id_rsa'
    host = 'rhswiwi7.ur.de'
    port = 222
    user = 'root'
    remote_address = 'cit-mongo'
    remote_port = 27017

    # database and collection names
    reduced_cell_id_db = 'reducedCellIdDB'
    clean_col = 'clean_measurements'
    restructure_lte_col = 'restructure_lte'
    restructure_umts_col = 'restructure_umts'
    restructure_gsm_col = 'restructure_gsm'

    # folium values
    default_location = [49.0167, 12.1010]

    # list of tiles
    tile_stamen_toner = 'Stamen Terrain'
    tile_stamen_watercolor = 'Stamen Watercolor'
    tile_open_street_map = 'OpenStreetMap'
    tile_carto_db_dark = 'CartoDB dark_matter'

    # colors
    dark_green = '#00b050'
    green = '#92d050'
    yellow = '#ffff00'
    orange = '#ffc000'
    dark_orange = '#f79646'
    red = '#ff0000'
    dark_red = '#c00000'

    # mobile network types
    lte = 'LTE'
    umts = 'UMTS'
    gsm = 'GSM'

    # mobile network
    allNetworks = '0'
    telekom = '1'
    vodafone = '2'
    telefonica = '3'

    # log configurations
    log_date_format = '%Y-%m-%d %H:%M:%S'
    log_format = '%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s'
    log_level = logging.DEBUG

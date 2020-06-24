class Config(object):
    # database connection data
    key = 'id_rsa'
    host = 'rhswiwi7.ur.de'
    port = 222
    user = 'root'
    remote_address = 'cit-mongo'
    remote_port = 27017

    # database and collection names
    reduced_cell_id_db = 'reducedCellIdDB'
    measurements_col = 'measurements'
    clean_col = 'clean_measurements'
    restructure_lte_col = 'restructure_lte'
    restructure_umts_col = 'restructure_umts'
    restructure_gsm_col = 'restructure_gsm'

    # attributes
    age = 3000.0
    accuracy = 13.0
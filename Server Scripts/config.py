class Config(object):
    # database connection data
    key = 'id_rsa'
    host = 'rhswiwi7.ur.de'
    port = 222
    user = 'root'
    remote_address = 'cit-mongo'
    remote_port = 27017
    api_token = 'beaa02b2a5307c'

    # database and collection names
    reduced_cell_id_db = 'reducedCellIdDB'
    measurements_col = 'measurements'
    clean_col = 'clean_measurements'
    restructure_lte_col = 'restructure_lte'
    restructure_umts_col = 'restructure_umts'
    restructure_gsm_col = 'restructure_gsm'
    unique_cell_identities_col = 'unique_cell_identities'
    cell_tower_locations_col = 'cell_tower_locations'

    # attributes
    age: float = 3000.0
    accuracy: float = 13.0

    min_mcc: int = 202
    max_mcc: int = 901

    min_mnc: int = 0
    max_mnc: int = 999

    min_lac: int = 0
    max_lac: int = 65533

    min_cid: int = 0
    max_cid_umts_lte: int = 268435455
    max_cid_gsm: int = 65535

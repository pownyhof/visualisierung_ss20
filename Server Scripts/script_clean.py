import time

from config import Config
from connector import Connector

start_time = time.time()

# connect to local database
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client['test']

# connect to server
client = Connector()
client.connect()
db = client.db

# empty destination collection to avoid conflicts
clean_col = db[Config.clean_col]
clean_col.delete_many({})
print('Deleted old collection')

# clone source collection to destination collection
measurements_col = db[Config.measurements_col]
measurements_col.aggregate([{'$out': Config.clean_col}])
print('Cloned collection')
print('Documents in total: ' + str(clean_col.count_documents({})))

# delete all documents that have an old version
clean_col.delete_many(
    {'$or': [{'version': 'pre-alpha'}, {'version': 'beta'}, {'version': 'b8d0d7f'}, {'version': '8e71d65'},
             {'version': 'd9db0ed'}, {'version': '9ec6b2c'}]})
print('Deleted all documents with older versions')
print('Remaining documents: ' + str(clean_col.count_documents({})))

# delete all documents with insufficient age and accuracy
clean_col.delete_many(
    {'$or': [{'location_information.age': {'$gte': Config.age}},
             {'location_information.age': {'$lte': Config.age * -1}},
             {'location_information.accuracy': {'$gte': Config.accuracy}}]})
print('Deleted all documents that have insufficient age and accuracy')
print('Remaining documents: ' + str(clean_col.count_documents({})))

# remove cell_info objects that are not active
clean_col.update_many({}, {'$pull': {'cell_info': {'active': False}}})
print('Removed all cell_info with active = false')
print('Remaining documents: ' + str(clean_col.count_documents({})))

# remove documents that have no active cell_info anymore
# CAUTION has to be executed after updating cell_info objects that are no active
clean_col.delete_many({'cell_info.active': {'$ne': True}})
print('Removed all documents that have no active cell_info anymore')
print('Remaining documents: ' + str(clean_col.count_documents({})))

# delete documents if the mobile_country_code is not within the sequence [202, ..., 901]
clean_col.delete_many(
    {'$or': [{'cell_info.$[].cell_identity.mobile_country_code': {'$lte': Config.min_mcc}},
             {'cell_info.$[].cell_identity.mobile_country_code': {'$gte': Config.max_mcc}}]})

# delete documents if the mobile_network_code is not within the sequence [0, ..., 999]
clean_col.delete_many(
    {'$or': [{'cell_info.$[].cell_identity.mobile_network_code': {'$lte': Config.min_mnc}},
             {'cell_info.$[].cell_identity.mobile_network_code': {'$gte': Config.max_mnc}}]})

# delete documents if the location_area_code is not within the sequence [0, ..., 65533]
clean_col.delete_many(
    {'$or': [{'cell_info.$[].cell_identity.location_area_code': {'$lte': Config.min_lac}},
             {'cell_info.$[].cell_identity.location_area_code': {'$gte': Config.max_lac}}]})

# delete documents if the cell_id is not within the sequence [0, ..., 65535] for the cell_info.type 'GSM' and
# [0, ..., 268435455] for the cell_info.type 'LTE' and 'UMTS'
clean_col.delete_many(
    {'cell_info.$[].cell_identity.cell_id': {'$lte': Config.min_cid}})
if 'cell_info.$[].type' == 'GSM':
    clean_col.delete_many(
        {'cell_info.$[].cell_identity.cell_id': {'$gte': Config.max_cid_gsm}})
elif 'cell_info.$[].type' == 'LTE':
    clean_col.delete_many(
        {'cell_info.$[].cell_identity.cell_id': {'$gte': Config.max_cid_umts_lte}})
elif 'cell_info.$[].type' == 'UMTS':
    clean_col.delete_many(
        {'cell_info.$[].cell_identity.cell_id': {'$gte': Config.max_cid_umts_lte}})
print('Removed all documents with invalid location_identity')
print('Remaining documents: ' + str(clean_col.count_documents({})))

# remove unnecessary field 'source_id'
clean_col.update_many({}, {'$unset': {'source_id': ''}})
print('Removed the field "source_id"')

# remove unnecessary field 'battery'
clean_col.update_many({}, {'$unset': {'battery': ''}})
print('Removed the field "battery"')

# remove unnecessary field 'location_information.altitude'
clean_col.update_many({}, {'$unset': {'location_information.altitude': ''}})
print('Removed the field "location_information.altitude"')

# remove unnecessary fields of 'cell.info.cell_identity'
clean_col.update_many({}, {'$unset':
                               {'cell_info.$[].cell_identity.basestation_id': '',
                                'cell_info.$[].cell_identity.basestation_identity_code': '',
                                'cell_info.$[].cell_identity.network_id': '',
                                'cell_info.$[].cell_identity.system_id': '',
                                'cell_info.$[].cell_identity.absolute_radio_frequency_channel_number': '',
                                'cell_info.$[].cell_identity.utra_absolute_radio_frequency_channel_number': '',
                                'cell_info.$[].cell_identity.e_utra_absolute_radio_frequency_channel_number': ''
                                }})
print('Removed unnecessary fields of "cell_info.cell_identity"')

# remove unnecessary fields of 'cell.info.cell_signal_strength'
clean_col.update_many({}, {'$unset':
                               {'cell_info.$[].cell_signal_strength.asu': '',
                                'cell_info.$[].cell_signal_strength.timing_advance_radio': '',
                                'cell_info.$[].cell_signal_strength.channel_quality_indicator': '',
                                'cell_info.$[].cell_signal_strength.reference_signal_received_power': '',
                                'cell_info.$[].cell_signal_strength.reference_signal_received_quality': '',
                                'cell_info.$[].cell_signal_strength.reference_signal_signal_to_noise_ratio': ''
                                }})
print('Removed all fields of "cell_signal_strength" except "dbm"')
print('Remaining documents: ' + str(clean_col.count_documents({})))

# remove documents with missing or empty fields (lac, mnc, mcc, cid)
clean_col.delete_many(
    {"$or": [
        {"cell_info.0.cell_identity.location_area_code": {"$exists": False}},
        {"cell_info.0.cell_identity.mobile_country_code": {"$exists": False}},
        {"cell_info.0.cell_identity.mobile_network_code": {"$exists": False}},
        {"cell_info.0.cell_identity.cell_id": {"$exists": False}},
    ]}
)
print('Removed all documents with missing or empty cel_identity fields')
print('Operation finished. Remaining documents: ' + str(clean_col.count_documents({})))

# disconnect from server
if type(client) == Connector:
    client.disconnect()

print("--- %s seconds ---" % (time.time() - start_time))
exit()

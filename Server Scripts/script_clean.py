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
print('Removed all cell_infos with active = false')
print('Remaining documents: ' + str(clean_col.count_documents({})))

# remove documents that have no active cell_infos anymore
# CAUTION has to be executed after updating cell_info objects that are no active
clean_col.delete_many({'cell_info.active': {'$ne': True}})
print('Removed all documents that have no active cell_infos anymore')
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

print('Operation finished. Remaining documents: ' + str(clean_col.count_documents({})))

# disconnect from server
if type(client) == Connector:
    client.disconnect()

print("--- %s seconds ---" % (time.time() - start_time))
exit()

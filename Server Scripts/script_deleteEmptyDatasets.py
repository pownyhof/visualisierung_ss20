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

clean_col = db[Config.clean_col]

# remove documents with missing or empty fields (lac, mnc, mcc, cid)
clean_col.delete_many({
    '$or': [
        {'cell_info.0.cell_identity.location_area_code': {'$exists': False}},
        {'cell_info.0.cell_identity.mobile_country_code': {'$exists': False}},
        {'cell_info.0.cell_identity.mobile_network_code': {'$exists': False}},
        {'cell_info.0.cell_identity.cell_id': {'$exists': False}}
    ]}
)

print('Remaining documents: ' + str(clean_col.count_documents({})))

# disconnect from server
if type(client) == Connector:
    client.disconnect()

print("--- %s seconds ---" % (time.time() - start_time))
exit()
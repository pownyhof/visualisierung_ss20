import time

from config import Config
from connector import Connector

start_time = time.time()

# connect to local database
# client = pymongo.MongoClient('mongodb://localhost:27017/')
# db = client['test']

# connect to server
client = Connector()
client.connect()
db = client.db

# empty destination collections to avoid conflicts
unique_cell_identities = db[Config.unique_cell_identities_col]
unique_cell_identities.delete_many({})
print('Deleted unique cell identities collection')


# creates a comparable tower id for api call usage
def create_id_tower(typ, mcc, mnc, lac, cid):
    return str(typ) + '-' + str(mcc) + '-' + str(mnc) + '-' + str(lac) + '-' + str(cid)


# takes all documents and puts them in the square structure
def cleanse_cell_identities(docs):
    # list has to be sorted
    docs = sorted(docs, key=lambda y: y['_id'])

    c = 0
    for _ in docs:
        while docs[c]['_id'] == docs[c + 1]['_id']:
            docs.pop(c + 1)
            if len(docs) == (c + 1):
                print('Documents haven been successfully sorted and cleansed')
                break
        c = c + 1
        if len(docs) == (c + 1):
            print('Documents haven been successfully sorted and cleansed')
            break
        return docs


# puts the documents into the database
def insert_documents_into_db(collection, list):
    for document in list:
        collection.insert_one(document)


cell_identities_list = []
other_list = []
clean_col = db[Config.clean_col]

# takes all documents and assigns them to the corresponding list with all needed information
for x in clean_col.find({}, {'_id': 0,
                             'cell_info.type': 1,
                             'cell_info.cell_identity.location_area_code': 1,
                             'cell_info.cell_identity.mobile_network_code': 1,
                             'cell_info.cell_identity.mobile_country_code': 1,
                             'cell_info.cell_identity.cell_id': 1,
                             }):
    typ = x['cell_info'][0]['type']
    mcc = int(x['cell_info'][0]['cell_identity']['mobile_country_code'])
    mnc = int(x['cell_info'][0]['cell_identity']['mobile_network_code'])
    lac = int(x['cell_info'][0]['cell_identity']['location_area_code'])
    cid = int(x['cell_info'][0]['cell_identity']['cell_id'])

    id_tower = create_id_tower(typ, mcc, mnc, lac, cid)

    doc = {'_id': id_tower,
           'cell_identity': [{'type': typ,
                              'mcc': mcc,
                              'mnc': mnc,
                              'lac': lac,
                              'cid': cid
                              }],
           }

    if typ == 'LTE':
        cell_identities_list.append(doc)
    elif typ == 'UMTS':
        cell_identities_list.append(doc)
    elif typ == 'GSM':
        cell_identities_list.append(doc)
    else:
        other_list.append(doc)

cell_identities_list = cleanse_cell_identities(cell_identities_list)
if len(other_list) > 0:
    print('WARNING: ' + str(len(other_list)) + ' documents could not be assigned to the cell_tower collection')
print('--- %s seconds ---' % (time.time() - start_time))

# insert squares into database
insert_documents_into_db(unique_cell_identities, cell_identities_list)
print('Number of unique cell_tower-documents in collection: ' + str(unique_cell_identities.count_documents({})))

print('Operation finished')

# disconnect from server
if type(client) == Connector:
    client.disconnect()

print('--- %s seconds ---' % (time.time() - start_time))
exit()
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
restructure_lte = db[Config.restructure_lte_col]
restructure_lte.delete_many({})
print('Deleted LTE collection')

restructure_umts = db[Config.restructure_umts_col]
restructure_umts.delete_many({})
print('Deleted UMTS collection')

restructure_gsm = db[Config.restructure_gsm_col]
restructure_gsm.delete_many({})
print('Deleted GSM collection')


# takes coordinates as int and transforms them into the unique id_geo
# example: (49.0229, 12.0796) -> 4902290120796
def create_id_geo(latitude, longitude):
    return (latitude.replace('.', '')) + '0' + (longitude.replace('.', ''))

# seperate timestampt into date and time
#def create_date(tim):
 #   return tim[:10]

#def create_time(tim):
 #   return tim[14:19]

# creates a comparable tower id for api call usage
def create_id_tower(typ, mcc, mnc, lac, cid):
    return str(typ) + '-' + str(mcc) + '-' + str(mnc) + '-' + str(lac) + '-' + str(cid)


# takes all documents and puts them in the square structure
def restructure_to_squares(docs):
    # list has to be sorted
    docs = sorted(docs, key=lambda y: y['id_geo'])

    c = 0
    for _ in docs:
        while docs[c]['id_geo'] == docs[c + 1]['id_geo']:
            docs[c]['square_data'].append(docs[c + 1]['square_data'][0])
            docs.pop(c + 1)
            if len(docs) == (c + 1):
                break
        c = c + 1
        if len(docs) == (c + 1):
            break

    return docs


# puts the squares into the database
def insert_documents_into_db(collection, square_list):
    for square in square_list:
        collection.insert_one(square)


lte_list = []
umts_list = []
gsm_list = []
other_list = []
clean_col = db[Config.clean_col]

# takes all documents and assigns them to the corresponding list with all needed information
for x in clean_col.find({}, {'_id': 0, 'timestamp': 1, 'location_information.latitude': 1,
                             'location_information.longitude': 1,
                             'location_information.accuracy': 1, 'location_information.age': 1,
                             'cell_info.type': 1,
                             'cell_info.cell_identity.cell_id': 1,
                             'cell_info.cell_identity.location_area_code': 1,
                             'cell_info.cell_identity.mobile_country_code': 1,
                             'cell_info.cell_identity.mobile_network_code': 1,
                             'cell_info.cell_signal_strength.dbm': 1}):
    tim = x['timestamp']
    lat = '{:.4f}'.format(x['location_information']['latitude'])
    lng = '{:.4f}'.format(x['location_information']['longitude'])
    acc = x['location_information']['accuracy']
    age = x['location_information']['age']
    typ = x['cell_info'][0]['type']
    cid = int(x['cell_info'][0]['cell_identity']['cell_id'])
    lac = int(x['cell_info'][0]['cell_identity']['location_area_code'])
    mcc = int(x['cell_info'][0]['cell_identity']['mobile_country_code'])
    mnc = int(x['cell_info'][0]['cell_identity']['mobile_network_code'])
    dbm = int(x['cell_info'][0]['cell_signal_strength']['dbm'])
    id_geo = create_id_geo(lat, lng)
    id_tower = create_id_tower(typ, mcc, mnc, lac, cid)
    doc = {'id_geo': id_geo,
           'latitude': float(lat),
           'longitude': float(lng),
           'square_data': [{'dbm': dbm,
                            'type': typ,
                            'time': tim,
                            'id_tower': id_tower,
                            'accuracy': acc,
                            'age': age}],
           'cell_tower': [{
               'lac': lac,
               'cid': cid,
               'mcc': mcc,
               'mnc': mnc
           }]}

    if typ == 'LTE':
        lte_list.append(doc)
    elif typ == 'UMTS':
        umts_list.append(doc)
    elif typ == 'GSM':
        gsm_list.append(doc)
    else:
        other_list.append(doc)

print('Number of documents with LTE: ' + str(len(lte_list)))
print('Number of documents with UMTS: ' + str(len(umts_list)))
print('Number of documents with GSM: ' + str(len(gsm_list)))
if len(other_list) > 0:
    print('WARNING: some documents could not be assigned to LTE, UMTS or GSM')
print('--- %s seconds ---' % (time.time() - start_time))

# restructure all documents to squares
lte_list = restructure_to_squares(lte_list)
print('Restructured LTE documents. Number of unique squares: ' + str(len(lte_list)))

umts_list = restructure_to_squares(umts_list)
print('Restructured UMTS documents. Number of unique squares: ' + str(len(umts_list)))

gsm_list = restructure_to_squares(gsm_list)
print('Restructured GSM documents. Number of unique squares: ' + str(len(gsm_list)))
print('--- %s seconds ---' % (time.time() - start_time))

# insert squares into database
insert_documents_into_db(restructure_lte, lte_list)
print('Squares in LTE collection: ' + str(restructure_lte.count_documents({})))

insert_documents_into_db(restructure_umts, umts_list)
print('Squares in UMTS collection: ' + str(restructure_umts.count_documents({})))

insert_documents_into_db(restructure_gsm, gsm_list)
print('Squares in GSM collection: ' + str(restructure_gsm.count_documents({})))

print('Operation finished')

# disconnect from server
if type(client) == Connector:
    client.disconnect()

print('--- %s seconds ---' % (time.time() - start_time))
exit()

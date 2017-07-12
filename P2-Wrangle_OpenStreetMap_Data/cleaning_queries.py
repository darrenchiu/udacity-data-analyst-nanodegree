from pymongo import MongoClient
import pprint

client = MongoClient('mongodb://localhost:27017/')
db = client.openstreetmap


# Part 1: Remove mainland China nodes
def find_nodes_with_details(query):
    locations = db.hk.find(query)
    # for location in locations:
    #     pprint.pprint(location)
    print(locations.count())


def delete_nodes(query):
    result = db.hk.delete_many(query)
    print(result.deleted_count)


# for mainland china locations
mainland_china_node_query = {
    "type": "node",
    '$or': [
        {"lat": {"$lt": 22.08}},
        {"lat": {"$gt": 22.35}},
        {"lon": {"$lt": 113.49}},
        {"lon": {"$gt": 114.31}},
    ]
}
find_nodes_with_details(mainland_china_node_query)
delete_nodes(mainland_china_node_query)

# Part 2: Clean up road names
result = db.hk.distinct("addr:street")

middle_replacement_map = {
    'Rd': 'Road',
    'Road1': 'Road',
    'Street2': 'Street',
    ', Wan Chai': '',
    ', Yau Ma Tei, Kowloon': '',
    ', Tai Wai, Shatin': '',
}

end_replacement_map = {
    'St': 'Street',
    'Smithfield': 'Smithfield Road',
}

for key in middle_replacement_map.keys():
    result = db.hk.find({"addr:street": {"$regex": '.*{}.*'.format(key)}})
    for location in result:
        pprint.pprint(location)
        location['addr:street'] = location['addr:street'].replace(key, middle_replacement_map[key])
        db.hk.save(location)
        pprint.pprint(location)

    print(result.count())

for key in end_replacement_map.keys():
    result = db.hk.find({"addr:street": {"$regex": '.*{}$'.format(key)}})
    for location in result:
        pprint.pprint(location)
        location['addr:street'] = location['addr:street'].replace(key, end_replacement_map[key])
        db.hk.save(location)
        pprint.pprint(location)

    print(result.count())

# special case that need escape character in regex
result = db.hk.find({"addr:street": {"$regex": '.*St\.$'}})
for location in result:
    pprint.pprint(location)
    location['addr:street'] = location['addr:street'].replace('St.', 'Street')
    db.hk.save(location)
    pprint.pprint(location)

print(result.count())

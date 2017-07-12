from pymongo import MongoClient
import pprint

client = MongoClient('mongodb://localhost:27017/')
db = client.openstreetmap

# Number of nodes
all_nodes = db.hk.find({"type": "node"})
print("Number of nodes: {}".format(all_nodes.count()))

# Number of ways
all_ways = db.hk.find({"type": "way"})
print("Number of ways: {}".format(all_ways.count()))

# Number of unique users
all_users = db.hk.distinct("user")
print("Number of distinct users: {}".format(len(all_users)))

# Number of natural nodes
all_natual_types = db.hk.distinct("natural")

pipeline = [{
    "$group": {
        "_id": "$natural",
        "count": {"$sum": 1}
    }
}]

results = db.hk.aggregate(pipeline)
for result in results:
    print(result)

# Number of HAD office
had_offices = db.hk.find({"name": {"$regex": '.*民政.*'}})
for office in had_offices:
    pprint.pprint(office['name'])
print("Number of HAD offices: {}".format(had_offices.count()))

# Number of railway stations
all_railway_stations = db.hk.find({"railway": 'station', "network": "MTR"})
for station in all_railway_stations:
    pprint.pprint(station['name'])
print("Number of railway stations: {}".format(all_railway_stations.count()))

# Number of Apple Stores
apple_stores = db.hk.find({"name": {"$regex": '.*Apple Store.*'}})
for store in apple_stores:
    pprint.pprint(store)
print("Number of apple stores: {}".format(apple_stores.count()))

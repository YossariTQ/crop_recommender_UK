import pymongo as pm

class MongoConnection:
    
    def __init__(self, URI, database_name, crop_collection_name):
        
        # Mongo Atlas 
        URI = 'mongodb://kbcrs:yorkirp@ac-xib4iiz-shard-00-00.u4ryiau.mongodb.net:27017,ac-xib4iiz-shard-00-01.u4ryiau.mongodb.net:27017,ac-xib4iiz-shard-00-02.u4ryiau.mongodb.net:27017/?ssl=true&replicaSet=atlas-fy2az9-shard-0&authSource=admin&retryWrites=true&w=majority'

        self.mongoClient = pm.MongoClient(URI)
        self.cropsDB = self.mongoClient[database_name]
        self.cropsCollection = self.cropsDB[crop_collection_name]
    
        connection = (f"""A connection has been established with the database and crop collection.

The following crops are viable given your location's predicted environmental and soil profile for 2023. 

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
""")
        
        print(connection)
    
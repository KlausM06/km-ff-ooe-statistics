from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

#retrieving the Mongodb connection String from the environment variable or enter it manually
client = MongoClient(os.getenv("MDB_URI","your-mongodb-connection-string"), server_api=ServerApi("1"))

# enter your database name
db = client["ff-statistics"]

# enter the name of your collections containing the operations, departments, logs etc.
oper_coll = db["operations"]
logs_coll = db["logs"]
deps_coll = db["departments"]
dist_coll = db["districts"]
opty_coll = db["operation_types"]
vill_coll = db["villages"]
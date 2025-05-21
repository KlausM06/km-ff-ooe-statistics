from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import BulkWriteError
import os

#retrieving the Mongodb connection String from the environment variable or enter it manually
client = MongoClient(os.getenv("MDB_URI","your-mongodb-connection-string"), server_api=ServerApi("1"))

# enter your database name
db = client["ff-statistics"]
# enter the name of your collection containing the operations
operations_coll = db["operations"]

def insert_operations(operations: list):
    """
    This function inserts a list of operations into the database.
    It will skip any operations that have already been inserted into the database.
    :param operations: list of operations
    :return: None
    """
    try:
        operations_coll.insert_many(operations, ordered=False) # set ordered=False to allow for bulk write errors

        # if there were no duplicates:
        print(f"Inserted {len(operations_coll)} operations")

        # if there are duplicate keys in the operations, the insert_many function will raise a BulkWriteError
        # we catch this error and get the number of inserted and skipped operations
    except BulkWriteError as bwe:
        inserted_count = bwe.details["nInserted"]
        skipped_count = len(operations) - inserted_count
        print(f"Inserted {inserted_count} operations, skipped {skipped_count} operations due to duplicates.")
    except Exception as e:
        print(e)
    


def ping():
    try: 
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
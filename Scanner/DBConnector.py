import time
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
# enter the name of your collection containing logs if you want to use it
logs_coll = db["logs"]


def insert_operations(operations: list):
    """
    This function inserts a list of operations into the database.\n
    It will skip any operations that have already been inserted into the database.\n
    :param operations: list of operations
    :return: None
    """
    inserted_count = 0
    skipped_count = 0
    try:
        operations_coll.insert_many(operations, ordered=False) # set ordered=False to allow for bulk write errors

        # if there were no duplicates:
        print(f"Inserted {len(operations_coll)} operations")
        inserted_count = len(operations_coll)

        # if there are operations in the operation list, which are already in the database, 
        # the insert_many function will raise a BulkWriteError
        # we catch this error and get the number of inserted and skipped operations
    except BulkWriteError as bwe:
        inserted_count = bwe.details["nInserted"]
        skipped_count = len(operations) - inserted_count
        print(f"Inserted {inserted_count} operations, skipped {skipped_count} operations due to duplicates.")
    except Exception as e:
        print(e)
        return
    
    # create log entry
    log = {
        "inserted_count": inserted_count,
        "skipped_count": skipped_count,
        "total_operations": len(operations),
        "timestamp": (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    }
    insert_log(log)

    

def insert_log(log: dict):
    """
    This function inserts a log entry into the database.\n
    This function is deactived if you set the environment variable SCAN_doLog to something else than "true"\n
    :return: None
    """
    if os.getenv("SCAN_doLog","true") == "true":
        try:
            message = logs_coll.insert_one(log)
            print(f"Inserted log entry with id {message.inserted_id}")
        except Exception as e:
            print(e)


def ping():
    try: 
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
from DBConnection import *
from pymongo.errors import BulkWriteError

def detect_villages():
    """
    This function detects the all villages from the operations.\n
    It will save them to the villages collection and will skip those who are already saved.\n
    :return: none
    """
    try:
        operations = list(oper_coll.find({}))
        villages = []
        for op in operations:
            op_type = extract_village(op)
            villages.append(op_type)
        
        vill_coll.insert_many(villages, ordered=False)
        print(f"Found {len(villages)} new villages")
    except BulkWriteError as bwe:
        inserted_count = bwe.details["nInserted"]
        skipped_count = len(villages) - inserted_count
        print(f"Found {inserted_count} new villages, skipped {skipped_count} documents due to duplicates.")
    except Exception as e:
        print(e)
        return

def extract_village(operation):
    """
    Extracts the village from the operation data.
    :param operation: The operation document from the database.
    :return: A dictionary representing the village.
    """
    return {
        "name": operation["einsatzort"]
    }

detect_villages()
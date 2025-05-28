from DBConnection import *
from pymongo.errors import BulkWriteError

def detect_districts():
    """
    This function detects the all opertaion types from the operations.\n
    It will save them to the operation_types collection and will skip those who are already saved.\n
    :return: none
    """
    try:
        operations = list(oper_coll.find({}))
        districts = []
        for op in operations:
            op_type = extract_district(op)
            districts.append(op_type)
        
        dist_coll.insert_many(districts, ordered=False)
        print(f"Found {len(districts)} new operation types")
    except BulkWriteError as bwe:
        inserted_count = bwe.details["nInserted"]
        skipped_count = len(districts) - inserted_count
        print(f"Found {inserted_count} new districts, skipped {skipped_count} documents due to duplicates.")
    except Exception as e:
        print(e)
        return

def extract_district(operation):
    """
    Extracts the district from the operation data.
    :param operation: The operation document from the database.
    :return: A dictionary representing the district.
    """
    return {
        "_id": operation["bezirk"]["id"],
        "description": operation["bezirk"]["text"]
    }


detect_districts()
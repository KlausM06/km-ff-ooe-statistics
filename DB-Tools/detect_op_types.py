from DBConnection import *
from pymongo.errors import BulkWriteError

def detect_operation_types():
    """
    This function detects the all opertaion types from the operations.\n
    It will save them to the operation_types collection and will skip those who are already saved.\n
    :return: none
    """
    try:
        operations = list(oper_coll.find({}))
        operation_types = []
        for op in operations:
            op_type = extract_operation_type(op)
            operation_types.append(op_type)
        
        opty_coll.insert_many(operation_types, ordered=False)
        print(f"Found {len(operation_types)} new operation types")
    except BulkWriteError as bwe:
        inserted_count = bwe.details["nInserted"]
        skipped_count = len(operation_types) - inserted_count
        print(f"Found {inserted_count} new operation types, skipped {skipped_count} documents due to duplicates.")
    except Exception as e:
        print(e)
        return

def extract_operation_type(operation):
    """
    Extracts the operation type from the operation data.
    :param operation: The operation document from the database.
    :return: A dictionary representing the operation type.
    """
    return {
        "general_op_type": operation["einsatzart"],
        "description": operation["einsatztyp"]["text"]
    }

opty_coll.drop()  
opty_coll.create_index([("description", 1)], unique=True)
detect_operation_types()
from DBConnection import *
from pymongo.errors import BulkWriteError

def detect_departments():
    """
    This function detects the all fire departments from the operations.\n
    It will save them to the departments collection and will skip those who are already saved.\n
    :return: List of departments
    """
    try:
        operations = list(oper_coll.find({}))
        departments = []
        for op in operations:
            # all the departments in the operation
            deps_op = list(op["feuerwehrenarray"].values())
            deps_op = reformatDepartments(deps_op)
            departments.append(deps_op)

        departments = [item for sublist in departments for item in sublist]
        deps_coll.insert_many(departments, ordered=False)
        print(f"Found {len(departments)} new departments")

    # if some of the departments are already in the database, the insert_many function will raise a BulkWriteError
    # we catch this error and get the number of inserted and skipped operations
    except BulkWriteError as bwe:
        inserted_count = bwe.details["nInserted"]
        skipped_count = len(departments) - inserted_count
        print(f"Found {inserted_count} new departments, skipped {skipped_count} departments due to duplicates.")
    except Exception as e:
        print(e)
        return

def reformatDepartments(departments: list):
    for i in range(departments.__len__()):
        departments[i]["_id"] = departments[i]["fwnr"]
        del departments[i]["fwnr"]
    return departments

detect_departments()
from DBConnection import *

def clear_logs():
    """
    This function clears the logs collection in the database.\n
    It will delete all entries in the logs collection.\n
    :return: None
    """
    try:
        logs_coll.delete_many({})
        print("Cleared logs collection")
    except Exception as e:
        print(e)

clear_logs()
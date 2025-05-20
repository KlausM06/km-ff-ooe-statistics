from DBConnector import insert_operations, ping
import requests
import time

# This URL is used to fetch the operations from the ooelfv API
FF_API_URL = "https://cf-einsaetze.ooelfv.at/webext2/rss/json_2tage.txt"

def main():
    print("Scanner started")
    # check connection to the database
    ping()

    print("--------------------------------------------------------------------------------")
    while True:
        print("Fetching and inserting operations...")
        print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        fetchAndInsertOperations()
        print("--------------------------------------------------------------------------------")
        time.sleep(3600) # time in seconds to wait before fetching the operations again
        

def fetchAndInsertOperations():
    # fetch operations from the API
    operations = fetch_operations()

    # reformat the operations
    operations = reformatOperations(operations)

    # remove all operations that are of type "SELBST"
    # this is done to avoid inserting operations that are not relevant for the statistics
    operations = cleanOperations(operations,key="einsatzart", value="SELBST")

    # remove all operations that are not completed yet
    # this is done because otherwise the operations would never contain the time when the operation was completed
    # which is a critical part of the statistics
    # (maybe) TODO: implement a system to update the operations in the database when they are completed, 
    #               so that uncompleted operations can also be saved to the database
    operations = cleanOperations(operations,key="status", value="offen")


    # insert operations into the database
    if operations.__len__() > 0:
        insert_operations(operations)


def cleanOperations(operations: list,key: str = "einsatzart", value: str = "empty"):
    """
    This function removes all operations that where the given key is equal to the given value
    :param operations: list of operations
    :param key: key to check for
    :param value: value to check for
    :return: list of operations without the operations that have the given key and value
    """
    offset = 0 # offset which makes i step back when an operation is deleted because the list is shortened
    for i in range(operations.__len__()):
        if operations[i-offset][key] == value:
            del operations[i-offset]
            offset += 1
    return operations


def reformatOperations(operations: list):
    """
    This function reformats the operations to be more compact and have the _id key set as the operation id (instead of "num1")
    :param operations: list of operations
    :return: list of operations with the _id key set as the operation id (instead of "num1")
    """
    for i in range(operations.__len__()):
        operations[i] = operations[i]["einsatz"]
        operations[i]["_id"] = operations[i]["num1"]
        del operations[i]["num1"]
    return operations


def fetch_operations():
    """
    Fetch operations from the ooelfv API and return them as a list of dictionaries.
    :return: list of operations
    """
    print("Fetching operations from the API...")
    try:
        response = requests.get(FF_API_URL)
        response.raise_for_status()  # Raise an error for bad responses
        resp_body = response.json()
        print("Operations fetched successfully")

        # "einsaetze" is the key in the JSON response that contains the operations
        # The operations are stored in a dictionary with keys 0...100+, so we need to convert it to a list
        return list(resp_body["einsaetze"].values()) 
    except requests.exceptions.RequestException as e:
        print(f"Error fetching operations: {e}")
        return []



if __name__ == "__main__":
    main()
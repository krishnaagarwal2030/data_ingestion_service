"""
Core modules
"""
import requests
import pymongo
import os
import datetime
MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME")
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")
MONGODB_PORT = os.environ.get("MONGODB_PORT")
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE")
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION")
MONGODB_SERVER = os.environ.get("MONGODB_SERVER")
TIMEOUT = 1  # seconds

def _return_database_connection():
    """
    Internal function to return a collection obj
    :return:
    """

    client = pymongo.MongoClient(f"mongodb://{MONGODB_SERVER}:{MONGODB_PORT}/", username=MONGODB_USERNAME, password=MONGODB_PASSWORD)
    db = client["DataIngestionDb"]
    col = db["Data_Collection"]
    return client, col

def collect_data(data_source, timeout=TIMEOUT):
    """
    Collects data from data source
    :param data_source: url of data source
    :return: response_code, data
    """
    response_code = 200
    data = None
    try:
        data  = requests.get(data_source, timeout=timeout)
        data = data.json()
    except requests.exceptions.Timeout:
        print("Request timed out")
        response_code = 408 # timeout
    except Exception as e:
        response_code = 500 # internal server error
        print("Exception occurred while collecting data", e)

    return response_code, data

def transform_data(input_data, data_source):
    """
    Transforms given data
    :param input_data:
    :param data_source:
    :return:
    """
    response_code = 200
    output_data = {}
    try:
        output_data = {"data": input_data, "ingested_at": datetime.datetime.utcnow(), "source": data_source}
    except Exception as e:
        response_code = 500
        print("Exception occurred while transforming data", e)

    return response_code, output_data

def store_data(data):
    """
    Stores given data
    :param data: valid data
    :return:
    """
    response_code = 200
    try:
        client, collection_obj = _return_database_connection()
        result = collection_obj.insert_one(data)
        print(f"Inserted document ID: {result.inserted_id}")
        client.close()
    except Exception as e:
        response_code = 500
        print("Exception occurred while storing data", e)

    return response_code

def fetch_inserted_data():
    """
    Fetch last inserted data
    Note: Assuming latest data fetch is required. Requirements are not specific
    :return:
    """
    response_code = 200
    data = None
    try:
        client, collection_obj = _return_database_connection()
        data = collection_obj.find_one(sort=[('ingested_at', pymongo.DESCENDING)])
        client.close()
    except Exception as e:
        response_code = 500
        print("Exception occurred while fetching data", e)

    return response_code, data

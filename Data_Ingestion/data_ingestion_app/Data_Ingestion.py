"""
Data ingestion service
"""
import uvicorn
from fastapi import FastAPI, Body, status, Request
from fastapi.responses import JSONResponse
import requests
data_ingestion_app = FastAPI()
from core_modules import collect_data, transform_data, store_data, fetch_inserted_data

@data_ingestion_app.post("/v1/data_ingestion")
def data_ingestion():
    """
    API to collect, transform and store data
    :return:
    """
    data_source = "https://jsonplaceholder.typicode.com/posts"  # data source can be an api parameter to make api generic
    response, collected_data = collect_data(data_source, timeout=1)
    if response != 200:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'message': f'Unable to collect data from {data_source}'})
    response, transformed_data = transform_data(collected_data, data_source)
    if response != 200:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'message': f'Error transforming data from {data_source}'})
    response = store_data(transformed_data)
    if response != 200:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'message': f'Error storing data from {data_source}'})

    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': f'Data Ingestion Successful'})

@data_ingestion_app.get("/v1/retrieve_data")
def data_retrieval():
    """
    API to retrieve data
    :return:
    """
    response, data = fetch_inserted_data()
    if response != 200:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': f'Error fetching data'})
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': f'Data Retreived successfully', 'data': str(data)})


if __name__ == '__main__':
    uvicorn.run("Data_Ingestion:data_ingestion_app", port=8080, host='0.0.0.0', reload=True)


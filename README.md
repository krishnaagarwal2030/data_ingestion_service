# Cyderes Data Ingestion Service

## Pre-requisite

Linux machine, with docker and docker-compose installed

## How to run

Clone the repository
cd cyderes_data_ingestion/Data_Ingestion/build
docker-compose up --build -d

## Test api
curl --location --request POST 'http://{machine-ip}:8080/v1/data_ingestion'
curl --location 'http://{machine-ip}:8080/v1/retrieve_data'

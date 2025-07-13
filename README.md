# Cyderes Data Ingestion Service

---

## Pre-requisites

To run the Cyderes Data Ingestion Service, you'll need:

* A **Linux machine**
* **Docker** installed
* **Docker Compose** installed

---

## How to Run


1.  **Clone the repository**:
    ```bash
    git clone https://github.com/krishnaagarwal2030/data_ingestion_service.git
    ```
2.  **Go to build directory**:
    ```bash
    cd data_ingestion_service/Data_Ingestion/build/
    ```
3.  **Build and start service**:
    ```bash
    docker-compose up --build -d
    ```

---

## Test API

* **Ingest Data (POST request)**:
    ```bash
    curl --location --request POST 'http://{machine-ip}:8080/v1/data_ingestion'
    ```
    Replace `{machine-ip}` with the actual IP address of your Linux machine.

* **Retrieve Data (GET request)**:
    ```bash
    curl --location 'http://{machine-ip}:8080/v1/retrieve_data'
    ```

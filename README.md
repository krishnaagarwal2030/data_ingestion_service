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


## Run testcase

* **Run Unitest**:
	```bash
    docker exec -it data_ingestion bash
    ```
	```bash
    cd /testcase; Python unitest_data_ingestion.py
    ```

## Documentation

* **API docs**:
    ```bash
    http://{machine-ip}:8080/redoc
    ```


* **Tranformation logic**:
	* tranform_data() function receives 'input_data' and 'data_source' as paramter
	* It then creates a dictionary {'data': input_data, 'data_source': data_source, 'ingested_data': current_utc_datetime}
	* It returns the created dictionary

* **Database Schemea**:
	* MongoDB (No-SQL based database) used for the project because of the flexibity it offers, which is important for data transformation logic.
	* Database schema: 
		* _id : Unique document identifier
		* data: input data fetched from data source(Supports any data type)
		* data_source: data url (String)
		* ingested_date: utc date(Datetime format)

* **What trade-offs did you consider**:
	* Programming language - 
		Developed working prototype in python first, with the idea of switching to Go later, since project involves lot of other things like containerisation, testing, documentation(including detailed questionarie) and deployment.
		* Go
			* Pros:
				* Mandatory per requirement
				* Faster, Cleaner
			* Cons:
				* Very little knowledge, multiple unknowns like gin, db connection
				* Project may get stuck in initial phase, due to deadline.
		* Python
			* Pros:
				* Strong prior experience developing end-to-end applications
			* Cons:
				* Not recommended as per requirement
	* Database:
		* Used mongodb database because of below reasons:
			* MongoDB
				* No-SQL based, flexible schema
				* Can be adabted easily to any change in tranformation logic
			* PostgreSQL:
				* SQL based, rigid schema
				* Difficult to change later
	* Cloud platform:
		Used AWS because of familiarity.

* **What were the hardest parts to implement and why?**
	* Moving to Go and AWS deployment due to time constraint

* **What would you improve if you had more time?**
	* Use nginx for load-balancing
	* Used rabbimq, redis, celery for faster api response, with worker nodes doing actual processing in backend
	* Make it cloud native(EC2, Document-db, ECR)

* **How would you track the latest successful data ingestion? Describe your approach, including any challenges you anticipate, and the trade-offs involved.**
	* Approach -1
		* Latest successfull data ingestion can be fetched from DB directly based on ingested_date(descending) and appropriate action can be taken
		
	* Approach -2
		* Store a metadata on every successful ingestion carrying details like ingested record it and other details.
		* Metadata can be store in mongo in a separate collection or json or postgres
	* Trade-offs:
		* Multiple ingestion may run in parallel so we need to ensure concurrency and atomicity using try-except, unique ingestion id and timestamp


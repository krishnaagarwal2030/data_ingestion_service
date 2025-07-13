FROM python:3.10
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /data_ingestion_app
COPY ./data_ingestion_app /data_ingestion_app
COPY ./testcase /testcase
RUN pip3 install -r /data_ingestion_app/pip-requirements.txt
CMD ["python", "Data_Ingestion.py"]
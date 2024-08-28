FROM apache/airflow:2.9.2-python3.10
ADD requirements.txt .
ADD credentials-python-storage.json .
RUN pip install -r requirements.txt
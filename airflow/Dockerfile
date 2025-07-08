FROM python:3.12.10

WORKDIR /usr/src/air

COPY airflow.cfg /root/airflow/airflow.cfg
COPY requirements.txt requirements.txt
COPY start.sh start.sh

COPY dags /root/airflow/dags

# need screen for this one
RUN apt-get update && apt-get install -y screen
RUN apt-get install -y screen

# install airflow
RUN pip install "apache-airflow[celery]==2.10.5" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.5/constraints-3.12.txt"
RUN pip install --no-cache-dir -r requirements.txt

# modify entry point for custom container starting commands
ENTRYPOINT  ["/bin/bash"]

# the entry point command
CMD [ "start.sh" ]

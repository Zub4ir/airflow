# db start
echo '---> start db'
airflow db migrate

# create admin users
echo '---> create user'
airflow users create --username 'jordan.perterson' --firstname jordan --lastname perterson --role Admin --email 'jordan.perterson@gmail.co.za' --password 'jordan.perterson'

# start webserver in background
echo '---> start webserver screen'
screen -dmS air-webserver
echo '---> send to serve screen'
screen -S air-webserver -X stuff 'airflow webserver --port 8080\n'


# final command - serve
echo '---> starting final serve'
airflow scheduler

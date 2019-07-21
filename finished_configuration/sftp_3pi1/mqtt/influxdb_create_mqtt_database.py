from influxdb import InfluxDBClient
client = InfluxDBClient(host='localhost', port=8086)
client.create_database('mqtt_python')
# create_retention_policy(name, duration, replication, database=None, default=False)
client.create_retention_policy('one_day', '1d', '1', database='mqtt_python', default=True)
client.drop_retention_policy('autogen', database='mqtt_python')
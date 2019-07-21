# -*- coding: utf-8 -*-
"""Tutorial for using pandas and the InfluxDB client."""

import argparse
import pandas as pd

from influxdb import DataFrameClient

import pprint


class Influxdbhandler:

    def __init__(self, host='localhost', port=8086):
        user = 'root'
        password = 'root'
        dbname = 'mqtt_python'
        # Temporarily avoid line protocol time conversion issues #412, #426, #431.
        # protocol = 'json'

        self.client = DataFrameClient(host, port, user, password, dbname)

    def getmeasurement(self,measurement=None,where_time_range=None):
        if measurement is None:
            return "Select measurement"
        # print("Read DataFrame")
        # data = self.client.query("select pitch from lage")
        field_string = ''
        for field in measurement['measurement_fields']:
            # field_string += 'mean("{}") AS "mean_{}", '.format(field['measurement_field_id'],field['measurement_field_id'])
            field_string += '"{}", '.format(field['measurement_field_id'])

        field_string = field_string[:-2]
        tag_string = ''
        
        for k, v in measurement['measurement_tags'].items():
            tag_string += ' AND "{}"=\'{}\''.format(k,v)

        # query_string = 'SELECT '+field_string+' FROM "mqtt_python"."one_day"."lage" WHERE time > now() - 10s '+tag_string+' GROUP BY time(:interval:) FILL(null)'
        query_string = 'SELECT '+field_string+' FROM "mqtt_python"."one_day"."'+ measurement['measurement_influxdb_name'] +'" WHERE '+where_time_range+' '+tag_string+' FILL(null)'
        data = self.client.query(query_string)
        if measurement['measurement_influxdb_name'] in data:
            return data[measurement['measurement_influxdb_name']]
        else:
            print('temp hint: query string ({})'.format(query_string))
            return None
        # return query_string
        # return "hi"
        # return pprint.pformat(data)
        # self.client.query('SELECT mean("heading") AS "mean_heading", mean("pitch") AS "mean_pitch", mean("roll") AS "mean_roll" FROM "mqtt_python"."one_day"."lage" WHERE time > now() - 5m AND "device_id"=\'b8:27:eb:7d:5c:14\' AND "service_id"=\'service-b8-27-eb-7d-5c-14-lagesensor\' GROUP BY time(:interval:) FILL(null)')
        # self.client.query('SELECT mean("delay_received_msvalue") AS "mean_delay_received_msvalue", mean("pitch") AS "mean_pitch", mean("heading") AS "mean_heading" FROM "mqtt_python"."one_day"."lage" WHERE time > now() - 5m GROUP BY time(:interval:) FILL(null)')

    
        

# # def main(host='localhost', port=8086):
# def main(host='3pi1.local', port=8086):
#     """Instantiate the connection to the InfluxDB client."""
#     user = 'root'
#     password = 'root'
#     dbname = 'demo'
#     # Temporarily avoid line protocol time conversion issues #412, #426, #431.
#     protocol = 'json'

#     client = DataFrameClient(host, port, user, password, dbname)

#     print("Create pandas DataFrame")
#     df = pd.DataFrame(data=list(range(30)),
#                       index=pd.date_range(start='2014-11-16',
#                                           periods=30, freq='H'))

#     print("Create database: " + dbname)
#     client.create_database(dbname)

#     print("Write DataFrame")
#     client.write_points(df, 'demo', protocol=protocol)

#     print("Write DataFrame with Tags")
#     client.write_points(df, 'demo',
#                         {'k1': 'v1', 'k2': 'v2'}, protocol=protocol)

#     print("Read DataFrame")
#     client.query("select * from demo")

#     print("Delete database: " + dbname)
#     client.drop_database(dbname)


# def parse_args():
#     """Parse the args from main."""
#     parser = argparse.ArgumentParser(
#         description='example code to play with InfluxDB')
#     parser.add_argument('--host', type=str, required=False,
#                         default='localhost',
#                         help='hostname of InfluxDB http API')
#     parser.add_argument('--port', type=int, required=False, default=8086,
#                         help='port of InfluxDB http API')
#     return parser.parse_args()


# service = Lagesensor(service_name='Lagesensor',service_description='Lagesensor Wert wird geschickt',device_name="zpi1",device_id="b8:27:eb:7d:5c:14")

# measurement_influxdb_name = "lage"
# measurement = {
#     "measurement_name" : "Lagesensor am zpi1",
#     "measurement_influxdb_name" : measurement_influxdb_name,
#     "measurement_id" : service.service_id + "---" + measurement_influxdb_name,
#     "measurement_tags" : {
#         "device_name": service.device_name,
#         "device_id": service.device_id,
#         "service_name": service.service_name,
#         "service_id": service.service_id,
#         "sensor": "mpu6050",
#     },
#     "measurement_fields" : [
#         {
#             "measurement_field_name" : "Pitch-Achse",
#             "measurement_field_id" : "pitch",
#             "measurement_field_unit" : "Degree",
#         },
#         {
#             "measurement_field_name" : "Roll-Achse",
#             "measurement_field_id" : "roll",
#             "measurement_field_unit" : "Degree",
#         },
#     ]
# }


# if __name__ == '__main__':
#     influxdbhandler = Influxdbhandler()
#     influxdbhandler.getmeasurement(measurement,"time > now() - 1m")
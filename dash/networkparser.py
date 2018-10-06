# -*- coding: utf-8 -*-
# pylint: disable=E1101, C0103, C0412, W0611
import subprocess
import json
import pprint
import ast
import re
import time

from collections import OrderedDict

import datetime


import redis


import dash_html_components as dhc
import dash_core_components as dcc

redisClient = redis.StrictRedis(host='127.0.0.1',port=6379)

def getvis():
    cmd = ['sudo', 'batadv-vis', '-f', 'jsondoc']
    result = json.loads(subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8'))
    return result['vis']


def getclients(vis):
    vis = getvis()

    clients = {}

    for device in vis:

        for client in device['clients']:
            clients[client] = device['primary']
    return clients

def convert(data):
    if isinstance(data, bytes):  return data.decode('ascii')
    if isinstance(data, dict):   return dict(map(convert, data.items()))
    if isinstance(data, tuple):  return map(convert, data)
    return data

def getservices():
    stored = redisClient.hgetall("services")
    stored_converted = convert(stored)
    stored_converted_list = list(stored_converted.values())
    return stored_converted_list

def getservice(service_id):
    stored = redisClient.hget("services",service_id)
    stored_converted = convert(stored)
    service_json_string = stored_converted.replace("'", "\"")
    service_dict = json.loads(service_json_string)
    return service_dict

def getalfred(vis,topic):

    clients = getclients(vis)
    # sudo alfred -r 65 gets hostnames
    cmd = ['sudo', 'alfred', '-r', str(topic)]
    # result = json.loads(subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8'))
    result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
    
    resultlist = result.replace('\\x0a', '').rstrip().split("\n")
    # return resultlist
    hostnames = {}
    for line in resultlist:
        client, value = re.findall('"([^"]*)"', line)
        hostnames[clients[client]] = value

    return hostnames

def printservices(services):
    

    sort_order = ['service_name', 'service_description', 'service_id','device_name','device_id','service_path','service_start_time','time_last_info_msvalue','topics_published','topics_subscribed','measurements']
    # services_ordered = [OrderedDict(sorted(item.items(), key=lambda item: sort_order.index(item[0])))
    #                 for item in services]
    # data = {'Author': "joe", 'data': services_ordered}
    # return json.dumps(data, indent=4, separators=(',', ': '))

    output = ""

    for service in services:
        service_json_string = service.replace("'", "\"")
        service_dict = json.loads(service_json_string)
        service_ordered = OrderedDict(sorted(service_dict.items(), key=lambda item: sort_order.index(item[0])))
        # print(type(service))
        # print(sejson_acceptable_string = service.replace("'", "\"")
        # service_json = json.loads(json_acceptable_string)rvice['topics_subscribed'])
        # print(service)
        # 
        output += json.dumps(service_ordered, indent=4) + '\n'
    return output


def addservices(services, nodes, edges,current_time_ms):

    for service in services:
        # print(type(service))
        # print(service['topics_subscribed'])
        # print(service)
        json_acceptable_string = service.replace("'", "\"")
        service_json = json.loads(json_acceptable_string)
        # print(node['primary'])
        time_diff = round((current_time_ms - int(service_json['time_last_info_msvalue']))/1000.0,1)

        if time_diff <= 3:
            color = '#9BC53D' # green
        elif 3 < time_diff <= 10:
            color = '#FDE74C' # yellow
        else:
            color = '#E55934' # red

        new_label = service_json['service_name'] + '\n(last info ' + str(time_diff) + ' s ago)'
        new_node = {'id': service_json['service_id'], 'label': new_label, 'color':color}
        # new_node = {'id': device['primary'], 'label': hostnames[device['primary']]}
        nodes.append(new_node)

        # new_edge = {'arrows':'','id': 'device-' + service_json['device_id'] + '---' + service_json['service_id'], 'from': 'device-' + service_json['device_id'], 'to': service_json['service_id'],'length':1}
        # new_edge = {'arrows':'','id': 'device-' + service_json['device_id'] + '---' + service_json['service_id'], 'from': 'device-' + service_json['device_id'], 'to': service_json['service_id'],'length': 10}
        new_edge = {'arrows':'','id': 'device-' + service_json['device_id'] + '---' + service_json['service_id'], 'from': 'device-' + service_json['device_id'], 'to': service_json['service_id'],}
        edges.append(new_edge)




def parsenetwork():
    vis = getvis()
    hostnames = getalfred(vis,65)
    last_sent_time_ms = getalfred(vis,67)
    services = getservices()

    data = {}

    nodes = []
    edges = []

    current_time_ms = int(time.time()*1000)

    for device in vis:
        # print(node['primary'])
        time_diff = round((current_time_ms - int(last_sent_time_ms[device['primary']]))/1000.0,1)

        if time_diff <= 3:
            color = '#9BC53D' # green
        elif 3 < time_diff <= 10:
            color = '#FDE74C' # yellow
        else:
            color = '#E55934' # red

        new_label = hostnames[device['primary']] + '\n' + device['primary'] + '\n(last alfred ' + str(time_diff) + ' s ago)'
        new_node = {'id': 'device-' + device['primary'], 'label': new_label, 'color':color, 'shape':'box'}
        # new_node = {'id': device['primary'], 'label': hostnames[device['primary']]}
        nodes.append(new_node)

        for neighborinfo in device['neighbors']:
            new_edge = {'arrows':'to','label': neighborinfo['metric'],'id': 'device-' + device['primary'] + '---' + 'device-' + neighborinfo['neighbor'], 'from': 'device-' + device['primary'], 'to': 'device-' + neighborinfo['neighbor']}
            edges.append(new_edge)

    data['nodes'] = nodes
    data['edges'] = edges

    addservices(services,nodes,edges,current_time_ms)

    return data


def show_selected_service(selection):
    try:
        service_id = selection['nodes'][0]
    except:
        return 'Please select a service.'

    if not service_id.startswith('service-'):
        return 'Please select a service.'
    
    service_dict = getservice(service_id)

    service_markdown = '''
**Service name:** {}  
**Service description:** {}  
**Service start time:** {} (UTC)  
**Measurements:**  
'''.format(service_dict['service_name'],service_dict['service_description'],datetime.datetime.fromtimestamp(service_dict['service_start_time']/1000.0))

    if service_dict['measurements']:
        measurements_options = []
        for measurement in service_dict['measurements'].values():
            measurements_options.append({'label': measurement['measurement_name'], 'value': measurement['measurement_id']})
        
        measurements_dropdown = dcc.Dropdown(
            id='service-measurements-dropdown',
            options=measurements_options,
            value=measurements_options[0]['value'],
            clearable=False
        )

        output = dhc.Div([
                dhc.H1(service_dict['service_name']),
                dcc.Markdown(service_markdown),
                measurements_dropdown
            ])
    else:
        output = dhc.Div([
                dhc.H1(service_dict['service_name']),
                dcc.Markdown(service_markdown)
            ])

    return output

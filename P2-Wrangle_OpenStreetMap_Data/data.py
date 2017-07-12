#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import os, json

tree = ET.parse('hong-kong_china.osm')
root = tree.getroot()


# helper function to write an object to output json file
def append_record(record):
    with open('hong-kong_china_cleaned.json', 'a') as f:
        f.write(json.dumps(record, ensure_ascii=False))
        f.write(os.linesep)

# nodes
node_with_details_count = 0
nodes = root.findall('./node')

# converting the xml into json that can be imported to mongodb
for node in nodes:
    node_obj = {}

    tags = node.findall('./tag')
    # to count number of non-empty nodes
    if len(tags) > 0:
        node_with_details_count += 1

    node_obj['type'] = 'node'
    node_obj['id'] = node.attrib['id']
    node_obj['lat'] = float(node.attrib['lat'])
    node_obj['lon'] = float(node.attrib['lon'])
    node_obj['version'] = node.attrib['version']
    node_obj['timestamp'] = node.attrib['timestamp']
    node_obj['changeset'] = node.attrib['changeset']
    node_obj['uid'] = node.attrib['uid']
    node_obj['user'] = node.attrib['user']

    for tag in tags:
        node_obj[tag.attrib['k']] = tag.attrib['v']
    append_record(node_obj)

print(node_with_details_count)

# ways
way_with_details_count = 0
ways = root.findall('./way')

# converting the xml into json that can be imported to mongodb
for way in ways:
    way_obj = {}

    tags = way.findall('./tag')
    # to count number of non-empty ways
    if len(tags) > 0:
        way_with_details_count += 1

    way_obj['type'] = 'way'
    way_obj['id'] = way.attrib['id']
    way_obj['version'] = way.attrib['version']
    way_obj['timestamp'] = way.attrib['timestamp']
    way_obj['changeset'] = way.attrib['changeset']
    way_obj['uid'] = way.attrib['uid']
    way_obj['user'] = way.attrib['user']

    for tag in tags:
        way_obj[tag.attrib['k']] = tag.attrib['v']
    append_record(way_obj)

print(way_with_details_count)

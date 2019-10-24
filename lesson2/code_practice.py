# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 07:15:52 2019

@author: 75253
"""

from collections import defaultdict
import requests
import json
import math

def geo_distance(origin, destination):
    # 两地经纬度计算距离
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    """
    lon1, lat1 = origin
    lon2, lat2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

def search(graph,start,destination):
    pathes = [[0, start]]  # 将当前路径长度添加到路径列表的第一个元素

    while pathes:
        path = pathes.pop(0)
        froniter = path[-1]

        successsors = graph[froniter]

        for stop in successsors:
            if stop in path: continue  # check loop

            new_path = path + [stop]
            new_path[0] = path[0] + get_stop_distance(path[-1], stop)  # 直接更新新路径的长度
            pathes.append(new_path)

        pathes = sort_by_distance(pathes) # 按新路径长度长短排序
        # visited.add(froniter)
        if (pathes and (destination == pathes[0][-1])):
            return "->".join(pathes[0][1:])

def sort_by_distance(pathes):  # 优化了排序计算方法，避免了多次的重复计算
    def get_distance_of_path(path):
        return path[0]
    return sorted(pathes,key=get_distance_of_path)

def get_stop_distance(stop1,stop2):
    return geo_distance(stop_coords[stop1],stop_coords[stop2])

# get lines data through baidu api
# data_url = 'http://map.baidu.com/?qt=bsi&c=131&t=1469072745455'
# response = requests.get(data_url)
# response.encoding = 'utf-8'
# line_data = response.json()["content"]

# local file
data_file = './line_data.json'

with open(data_file, 'r', encoding='utf8') as fr:
   line_data = json.load(fr)["content"]
fr.close()

location_map = defaultdict(list)
stop_coords = {}
for line in line_data:
    stops = line["stops"]
    for stop in stops:
        stop_coords[stop['name']] = (float(stop['x']), float(stop['y']))
    for i in range(len(stops)-1):
        location_map[stops[i]["name"]].append(stops[i+1]["name"])

routes = search(location_map, '沙河', '双井')
print(routes)

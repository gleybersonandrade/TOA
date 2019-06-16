"""Traffic Occurrence Analyzer utils."""

# System imports
import codecs
import csv
import json
import os
import re

# Third-party imports
import gmplot
import networkx as nx

# Local imports
from config import (COLLECTIONS, FILES_FOLDER, GM_API_KEY, GM_LAT, GM_LEN,
                    GM_ZOOM, YEARS)


def save_json(data, path):
    """Save data to JSON file."""
    with open(path, 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True)


def read_json(path):
    """Read data from JSON file."""
    with open(path, 'r') as file:
        return json.load(file)


def construct():
    """Construct file to be used in graph."""
    def add(data, br, km, year, events):
        """Calculate critical level and insert events and in data dict."""
        if br not in data:
            data[br] = {}
        if km not in data[br]:
            data[br][km] = {}
        accidents = events.get("accidents") or 0
        deaths = events.get("deaths") or 0
        infractions = events.get("infractions") or 1
        critical = round((25 * deaths + 5 * accidents + 0.005 * infractions), 3)
        events.update({"critical": critical})
        current_critical = data[br][km].get("critical") or 0
        data[br][km][year] = events
        data[br][km]["critical"] = round(current_critical + critical /
                                         (int(YEARS[-1])-int(year)+1), 3)

    data = {}
    f_data = read_json(FILES_FOLDER + '/all.json')
    for br, kms in f_data.items():
        for km, years in kms.items():
            for year, events in years.items():
                if year in YEARS:
                    add(data, br, km, year, events)
                    data[br][km]["coordinates"] = f_data[br][km]["coordinates"]
    save_json(data, FILES_FOLDER + '/final.json')


def execute():
    """Make traffic occurrence graph."""
    def make_map(nodes):
        """Build the map with events."""
        gmap = gmplot.GoogleMapPlotter(GM_LAT, GM_LEN, GM_ZOOM)
        gmap.apikey = GM_API_KEY
        for node in nodes:
            args = {
                "title": node[0],
                "critical": node[1]["critical"],
                "lat": float(node[1]["lat"]),
                "lon": float(node[1]["lon"])
            }
            gmap.marker(args.get("lat"), args.get("lon"),
                        title=args.get("critical"))
        gmap.draw(FILES_FOLDER + 'map.html')

    G = nx.Graph()
    f_data = read_json(FILES_FOLDER + '/final.json')
    for br, kms in f_data.items():
        for km, values in kms.items():
            coordinates = values.get("coordinates")
            G.add_node(br+"-"+km,
                       critical=values.get("critical"),
                       lat=coordinates.get("lat"),
                       lon=coordinates.get("lon"))
    make_map(G.nodes.data())


def run(method):
    """Run method."""
    switcher = {
        "construct": lambda: construct(),
        "execute": lambda: execute()
    }
    return switcher.get(method)()

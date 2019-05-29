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


def generate():
    """Generate files."""
    def add(events, br, km, event):
        """Insert an event in events dict."""
        if br not in events:
            events[br] = {}
        if km not in events[br]:
            events[br][km] = {}
        for key in event:
            if key not in events[br][km]:
                events[br][km][key] = 0
            value = events[br][km][key] + event[key]
            events[br][km].update({key: value})

    def get_data(year):
        """Get data from CSV files."""
        def read_csv(path):
            """Read CSV file."""
            with codecs.open(path, 'r', encoding="utf-8",
                             errors="ignore") as file:
                reader = csv.reader(file, delimiter=';')
                header = next(reader, None)
                lines = [line for line in reader]
                file.close()
            return header, lines

        data = {}
        for key, values in COLLECTIONS.items():
            path = FILES_FOLDER + year + '/' + key
            files = [f for f in os.listdir(path)
                     if os.path.isfile(os.path.join(path, f))]
            file_data = []
            for file in files:
                header, lines = read_csv(path + '/' + file)
                for line in lines:
                    document = {}
                    for index, field in enumerate(header):
                        if field in values:
                            document.update({field: line[index]})
                    file_data.append(document)
            data[key] = file_data
        return data

    for year in YEARS:
        events = {}
        data = get_data(year)
        for accident in data["accidents"]:
            accidents = 1
            fatal_accidents = 0
            if int(accident["mortos"]) > 0:
                fatal_accidents = 1
                accidents = 0
            event = {"accidents": accidents,
                     "fatal_accidents": fatal_accidents}
            add(events, re.split('[,|.]', accident["br"])[0],
                re.split('[,|.]', accident["km"])[0], event)
        for infraction in data["infractions"]:
            event = {"infractions": 1}
            add(events, re.split('[,|.]', infraction["num_br_infracao"])[0],
                re.split('[,|.]', infraction["num_km_infracao"])[0], event)
        save_json(events, FILES_FOLDER + year + '/out.json')


def construct():
    """Construct file to be used in graph."""
    def add(data, br, km, year, events):
        """Calculate critical level and insert events and in data dict."""
        if br not in data:
            data[br] = {}
        if km not in data[br]:
            data[br][km] = {}
        accidents = events.get("accidents") or 0
        fatal_accidents = events.get("fatal_accidents") or 0
        infractions = events.get("infractions") or 1
        critical = round((3*fatal_accidents + accidents + 0.1*infractions), 3)
        events.update({"critical": critical})
        current_critical = data[br][km].get("critical") or 0
        data[br][km][year] = events
        data[br][km]["critical"] = round(current_critical + critical /
                                         (int(YEARS[-1])-int(year)+1), 3)

    data = {}
    for year in YEARS:
        file_data = read_json(FILES_FOLDER + year + '/out.json')
        for br, kms in file_data.items():
            for km, events in kms.items():
                add(data, br, km, year, events)
    save_json(data, FILES_FOLDER + '/out.json')


def execute():
    """Make traffic occurrence graph."""
    def make_map(nodes):
        """Build the map with events."""
        # gmplot helper commands:
        # https://gist.github.com/hhl60492/120362483890db9df622020eaea7c92e
        gmap = gmplot.GoogleMapPlotter(GM_LAT, GM_LEN, GM_ZOOM)
        gmap.apikey = GM_API_KEY
        for node in nodes:
            args = {
                "title": node[0],
                "lat": float(node[1]["lat"]),
                "lon": float(node[1]["lon"])
            }
            gmap.marker(args.get("lat"), args.get("lon"),
                        title=args.get("title"))
        gmap.draw(FILES_FOLDER + 'map.html')

    G = nx.Graph()
    file_data = read_json(FILES_FOLDER + '/all.json')
    for kms in file_data.values():
        for km, values in kms.items():
            coordinates = values.get("coordinates")
            G.add_node(km,
                       lat=coordinates.get("lat"),
                       lon=coordinates.get("lon"))
    make_map(G.nodes.data())


def run(method):
    """Run method."""
    switcher = {
        "generate": lambda: generate(),
        "construct": lambda: construct(),
        "execute": lambda: execute()
    }
    return switcher.get(method)()

"""Traffic Occurrence Analyzer config."""

GM_API_KEY = "secret"
GM_LAT = -15.135
GM_LEN = -51.9253
GM_ZOOM = 5

FILES_FOLDER = "files/"

COLLECTIONS = {"accidents": {"br", "km", "mortos"},
               "infractions": {"num_br_infracao", "num_km_infracao"}}

YEARS = ["2015", "2016", "2017", "2018"]

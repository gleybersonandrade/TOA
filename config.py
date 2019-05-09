"""Traffic Occurrence Analyzer config."""

DB_HOST = "localhost"
DB_PORT = 27017
DB_NAME = "toa"

DB_COLLECTIONS = {"accidents": {"br", "km", "mortos"},
                  "infractions": {"num_br_infracao", "num_km_infracao"}}

DB_SEPARATOR = "_"
FILES_FOLDER = "files/"
FILES_SEPARATOR = "/"
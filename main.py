#!/usr/bin/env python3
import configparser
import os
import sys
import math
import locale
import logging
import kodijsonrpc


def format_time(time: dict):
    return f'{time["hours"]}:{time["minutes"]:02d}:{time["seconds"]:02d}'


locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
if len(sys.argv) >= 2 and os.path.isdir(os.path.realpath(os.path.dirname(sys.argv[1]))):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s',
                        filename=sys.argv[1], filemode='a')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s',
                        stream=sys.stdout)
logging.getLogger('jsonrpcclient.server').setLevel(logging.WARNING)

configfile = f"{os.path.realpath(os.path.dirname(__file__))}/config.ini"
if not os.path.isfile(configfile):
    logging.log(logging.ERROR, f"{configfile} not found")
    exit(1)
config = configparser.ConfigParser()
config.read(configfile)

kodi = kodijsonrpc.KodiJSONClient(config["kodi"]["server"], int(config["kodi"]["port"]),
                                  config["kodi"]["user"], config["kodi"]["password"])
players = kodi.Player.GetActivePlayers()
for player in players:
    properties = kodi.Player.GetProperties({"playerid": player["playerid"],
                                            "properties": ["time", "totaltime", "percentage"]})
    playing = kodi.Player.GetItem({"playerid": player["playerid"],
                                   "properties": ["file", "duration", "runtime"]})
    logging.info(f'playing: {playing["item"]["label"]} - {format_time(properties["time"])} of '
                 f'{format_time(properties["totaltime"])} ({math.floor(properties["percentage"])}%)')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io
import websockets
from websocket import create_connection

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()


def msg_links_up(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    
    ws = create_connection("ws://192.168.178.102:8080")
    ws.send("Update GA:01_0_002=0")
    #result =  ws.recv()
    ws.close()

    if len(intentMessage.slots.house_room) > 0:
        house_room = intentMessage.slots.house_room.first().value # We extract the value from the slot "house_room"
        result_sentence = "Das Licht wird in {} angeschaltet".format(str(house_room))  # The response that will be said out loud by the TTS engine.
    else:
        result_sentence = "Links hoch"

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)

def msg_links_down(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    
    ws = create_connection("ws://192.168.178.102:8080")
    ws.send("Update GA:01_0_002=1")
    ws.close()

    if len(intentMessage.slots.house_room) > 0:
        house_room = intentMessage.slots.house_room.first().value # We extract the value from the slot "house_room"
        result_sentence = "Das Licht wird in {} ausgeschaltet".format(str(house_room))  # The response that will be said out loud by the TTS engine.
    else:
        result_sentence = "links runter"

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)
    
def msg_rechts_up(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    
    ws = create_connection("ws://192.168.178.102:8080")
    ws.send("Update GA:01_0_004=0")
    #result =  ws.recv()
    ws.close()

    if len(intentMessage.slots.house_room) > 0:
        house_room = intentMessage.slots.house_room.first().value # We extract the value from the slot "house_room"
        result_sentence = "Das Licht wird in {} angeschaltet".format(str(house_room))  # The response that will be said out loud by the TTS engine.
    else:
        result_sentence = "Rechts hoch"

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)

def msg_rechts_down(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    
    ws = create_connection("ws://192.168.178.102:8080")
    ws.send("Update GA:01_0_004=1")
    ws.close()

    if len(intentMessage.slots.house_room) > 0:
        house_room = intentMessage.slots.house_room.first().value # We extract the value from the slot "house_room"
        result_sentence = "Das Licht wird in {} ausgeschaltet".format(str(house_room))  # The response that will be said out loud by the TTS engine.
    else:
        result_sentence = "Rechts runter"

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)
    
def msg_fenster_up(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    
    ws = create_connection("ws://192.168.178.102:8080")
    ws.send("Update GA:01_0_006=0")
    #result =  ws.recv()
    ws.close()

    if len(intentMessage.slots.house_room) > 0:
        house_room = intentMessage.slots.house_room.first().value # We extract the value from the slot "house_room"
        result_sentence = "Das Licht wird in {} angeschaltet".format(str(house_room))  # The response that will be said out loud by the TTS engine.
    else:
        result_sentence = "Fenster hoch"

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)

def msg_fenster_down(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    
    ws = create_connection("ws://192.168.178.102:8080")
    ws.send("Update GA:01_0_006=1")
    ws.close()

    if len(intentMessage.slots.house_room) > 0:
        house_room = intentMessage.slots.house_room.first().value # We extract the value from the slot "house_room"
        result_sentence = "Das Licht wird in {} ausgeschaltet".format(str(house_room))  # The response that will be said out loud by the TTS engine.
    else:
        result_sentence = "Fenster runter"

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)
    
def msg_schlafen_down(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    
    ws = create_connection("ws://192.168.178.102:8080")
    ws.send("Update GA:01_0_006=1")
    ws.send("Update GA:01_0_002=1")
    ws.send("Update GA:01_0_004=1")
    ws.close()

    if len(intentMessage.slots.house_room) > 0:
        house_room = intentMessage.slots.house_room.first().value # We extract the value from the slot "house_room"
        result_sentence = "Das Licht wird in {} ausgeschaltet".format(str(house_room))  # The response that will be said out loud by the TTS engine.
    else:
        result_sentence = "alle runter"

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)
    
if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent("cetax:links_up", msg_links_up)
        h.subscribe_intent("cetax:links_down", msg_links_down)
        h.subscribe_intent("cetax:rechts_up", msg_rechts_up)
        h.subscribe_intent("cetax:rechts_down", msg_rechts_down)
        h.subscribe_intent("cetax:fenster_up", msg_fenster_up)
        h.subscribe_intent("cetax:fenster_down", msg_fenster_down)
        h.subscribe_intent("cetax:schlafen_down", msg_schlafen_down)
        h.start()

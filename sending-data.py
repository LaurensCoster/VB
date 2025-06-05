import functions_framework
import re
import copy
import json
import requests
from flask import jsonify
from datetime import datetime

def prepare_transcript(transcript):
    if len(transcript) < 3:
        return []

    print(transcript)
    transcript.append("nie")
    grouped = []

    for i in range(3):
        if "Mówi do Ciebie Voicebot" in transcript[i]:
            transcript = transcript[(i):]
            break
    print(transcript)


    for i in range(0, len(transcript) - 1, 2):
        grouped.append({"question": transcript[i], "answer": transcript[i + 1]})
    return grouped

@functions_framework.http
def hello_http(request):
    req = request.get_json(silent=True)
    tag = req.get("fulfillmentInfo", {}).get("tag")
    session_params = req.get('sessionInfo', {}).get('parameters', {})
    session_params['loop_counter'] = int(session_params.get('loop_counter', 1)) + 1
    if 'ilosc_pomieszczen' not in session_params or not session_params['ilosc_pomieszczen']:
        session_params['ilosc_pomieszczen'] = 1

    room_str = session_params.get("room", "{}")
    room_str = room_str[8:-3]
    print(f"START. Sesion: {session_params}")
    print(repr(room_str))

    try:
        room_json = json.loads(room_str)
        if not isinstance(room_json, dict):
            room_json = {}
    except:
        try:
            room_json = ast.literal_eval(room_str)
            if not isinstance(room_json, dict):
                room_json = {}
        except:
            print("Invalid JSON format in room parameter")
            json_response = {
                "sessionInfo": {
                    "parameters": session_params
                }
            }
            return json_response

    try:
        if "wymiary_zacieku_sufit" in session_params:
            session_params['wymiary_zacieku_sufit'] = float(session_params['wymiary_zacieku_sufit'])
        if "wymiary_zacieku_sciana" in session_params:
            session_params['wymiary_zacieku_sciana'] = float(session_params['wymiary_zacieku_sciana'])
        if "wysokosc_kafelki" in session_params:
            session_params['wysokosc_kafelki'] = float(session_params['wysokosc_kafelki'])
        if "wymiary_zacieku" in session_params:
            session_params['wymiary_zacieku'] = float(session_params['wymiary_zacieku'])
    except:
        print("Błąd zamiany parametru na wartość float")
    else_parameters_general = ['wymiary_zacieku']
    else_parameters_ceiling = ['halogeny_ilosc', 'miejsce_sufit', 'inne_sufit','wymiary_zacieku_sufit']
    else_parameters_wall = ['inne_sciana', 'rodzaj_farby', 'wysokosc_kafelki', 'wymiary_zacieku_sciana']
    else_parameters_floor = ['wykladzina', 'panele', 'inne_podloga']
    else_parameters_door = ['rodzaj_drzwi', 'uszkodzenia_drzwi', 'szerkosc_drzwi', 'wysokosc_drzwi', 'grubosc_drzwi']
    for param in else_parameters_general:
        if param in session_params:
            room_json[param] = session_params[param]
        else:
            room_json[param] = None
    if "nazwa_pomieszczenia" in session_params:
        room_json["name"] = session_params["nazwa_pomieszczenia"]
    else:
        room_json["nazwa_pomieszczenia"] = None
    for param in else_parameters_ceiling:
        if room_json["Ceiling"] is not None and param in session_params:
            room_json["Ceiling"][param] = session_params[param]
        elif room_json["Ceiling"] is not None:
            room_json["Ceiling"][param] = None
    for param in else_parameters_wall:
        if room_json["Wall"] is not None and param in session_params:
            room_json["Wall"][param] = session_params[param]
        elif room_json["Wall"] is not None:
            room_json["Wall"][param] = None
    for param in else_parameters_floor:
        if room_json["Floor"] is not None and param in session_params:
            room_json["Floor"][param] = session_params[param]
        elif room_json["Floor"] is not None:
            room_json["Floor"][param] = None
    for param in else_parameters_door:
        if room_json["Door"] is not None and param in session_params:
            room_json["Door"][param] = session_params[param]
        elif room_json["Door"] is not None:
            room_json["Door"][param] = None

    null_parameters = [
        'nazwa_pomieszczenia', 'dlugosc', 'szerokosc', 'wysokosc', 'ksztalt_zacieku', 'miejsce_zacieku', 'wymiary_zacieku', 'czy_mienie',
        'wykonczenie_sufit', 'halogeny_ilosc', 'miejsce_sufit', 'inne_sufit',
        'wykonczenie_sciana',  'inne_sciana', 'rodzaj_farby', 'kolor_farby', 'wysokosc_kafelki',
        'wykonczenie_podloga', 'wykladzina', 'panele', 'inne_podloga', 'podloga_uszkodzenie_procentowe', 'obszar_podloga',
        'rodzaj_drzwi', 'uszkodzenia_drzwi', 'szerkosc_drzwi', 'wysokosc_drzwi', 'grubosc_drzwi', 'room',
    ]
    
    for param in null_parameters:
        session_params[param] = None
    for key in list(session_params.keys()):  
        if key.startswith("mienie_ruchome"):  
            del session_params[key]

    if "rooms" not in session_params:
        session_params["rooms"] = []
    session_params["rooms"].append(room_json)
    if "ilosc_pomieszczen" not in session_params:
        session_params["ilosc_pomieszczen"] = 0
    if "id_szkody" not in session_params:
        session_params["id_szkody"] = 0
    if "okolicznosci" not in session_params:
        session_params["okolicznosci"] = None

    if tag == "disconnected" or session_params["loop_counter"] > int(session_params["ilosc_pomieszczen"]):
        if "transcription" in session_params:
            transcription = prepare_transcript(session_params["transcription"])
        else:
            return {}
        json_to_send = {
            "okolicznosci": session_params["okolicznosci"],
            "id_szkody": session_params["id_szkody"],
            "rooms": session_params["rooms"],
            "transcription": transcription,
            "czas_wyslania": datetime.now().isoformat()
        }
        
        if tag == "disconnected" and "failed_recording" in session_params:
            json_to_send["call_end"] = "failed_recording"
            json_to_send["rooms"] = []
        elif tag == "disconnected" and "failed_authentication" in session_params:
            json_to_send["call_end"] = "failed_authentication"
            json_to_send["rooms"] = []
        elif tag == "disconnected" and "okolicznosci_end" in session_params:
            json_to_send["call_end"] = "failed_circumstances"
            json_to_send["rooms"] = []
        elif tag == "disconnected":
            json_to_send["call_end"] = "disconnected"
        else:
            json_to_send["call_end"] = "natural_stop"
        print(json_to_send)

        url = "https://uat-mojaszkoda.mentax.pl/api/voicebot/create-message"
        headers = {
            "X-AUTH-TOKEN": "4d73d68af5834ba4911b74d53b332e9c",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url, headers=headers, json=json_to_send)
            print(response.status_code)    
        except Exception as e:
            print(f"Wystąpił błąd z wysyłaniem danych: {e}")
    
    print(session_params)
    json_response = {
        "sessionInfo": {
            "parameters": session_params
        }
    }
    return json_response

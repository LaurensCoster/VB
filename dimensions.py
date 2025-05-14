import functions_framework
import json

@functions_framework.http
def hello_http(request):
    req = request.get_json(silent=True)
    tag = req.get("fulfillmentInfo", {}).get("tag")
    session_params = req.get('sessionInfo', {}).get('parameters', {})
    dictionary = session_params.get(tag)
    dictionary = dictionary[8:-4]
    print(repr(dictionary))
    dictionary = json.loads(dictionary)

    session_params["dlugosc"] = dictionary["dlugosc"]
    session_params["szerokosc"] = dictionary["szerokosc"]
    session_params["wysokosc"] = dictionary["wysokosc"]
    session_params["wymiary"] = None

    response = {
        "sessionInfo": {
            "parameters": session_params
        }
    }
    return response

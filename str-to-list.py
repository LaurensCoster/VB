import functions_framework
import json


@functions_framework.http
def hello_http(request):
    req = request.get_json(silent=True)
    tag = req.get("fulfillmentInfo", {}).get("tag")
    session_params = req.get('sessionInfo', {}).get('parameters', {})
    lista = session_params.get(tag)
    print(repr(lista))
    lista = json.loads(lista)

    session_params[tag] = lista

    response = {
        "sessionInfo": {
            "parameters": session_params
        }
    }
    return response

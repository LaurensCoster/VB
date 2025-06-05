import functions_framework
import json

@functions_framework.http
def hello_http(request):
    req = request.get_json(silent=True)
    tag = req.get("fulfillmentInfo", {}).get("tag")
    session_params = req.get('sessionInfo', {}).get('parameters', {})
    lista = session_params.get(tag)
    print(repr(lista))
    try:
        lista = json.loads(lista)
    except:
        try:
            lista = ast.literal_eval(lista)
        except:
            lista = []
    print(lista)
    session_params[tag] = lista
    
    response = {
        "sessionInfo": {
            "parameters": session_params
        }
    }
    return response

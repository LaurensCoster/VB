import functions_framework
import json

@functions_framework.http
def hello_http(request):
    req = request.get_json(silent=True)
    session_params = req.get('sessionInfo', {}).get('parameters', {})
    circumstances  = session_params.get("okolicznosci_lista")
    print("xd")
    print(repr(circumstances))
    try:
        circumstances = json.loads(circumstances)
    except:
        try:
            circumstances = ast.literal_eval(circumstances)
        except:
            circumstances = []

    session_params["ilosc_pomieszczen"] = circumstances[0]
    session_params["nazwa_pomieszczenia"] = circumstances[1]
    session_params["okolicznosci_lista"] = None

    response = {
        "sessionInfo": {
            "parameters": session_params
        }
    }
    return response

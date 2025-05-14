import functions_framework


@functions_framework.http
def hello_http(request):
    req = request.get_json(silent=True)
    session_params = req.get('sessionInfo', {}).get('parameters', {})
    counter = session_params.get('counter', 1)
    rodzaj = session_params.get('rodzaj')
    model = session_params.get('model')
    data = session_params.get('data')
    charakter_uszkodzen = session_params.get('charakter_uszkodzen')
    lokalizacja_uszkodzen = session_params.get('lokalizacja_uszkodzen')

    mienie_ruchome_key = f"mienie_ruchome{int(counter)}"
    mienie_ruchome_value = {
        "rodzaj": rodzaj,
        "model": model,
        "data": data,
        "charakter_uszkodzen": charakter_uszkodzen,
        "lokalizacja_uszkodzen": lokalizacja_uszkodzen
    }
    print(mienie_ruchome_value)

    response = {
        "sessionInfo": {
            "parameters": {
                mienie_ruchome_key: mienie_ruchome_value,
                "rodzaj": None,
                "model": None,
                "data": None,
                "charakter_uszkodzen": None,
                "lokalizacja_uszkodzen": None,
                "counter": counter + 1
            }
        }
    }
    return response

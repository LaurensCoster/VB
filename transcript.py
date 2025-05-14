import functions_framework
import json

@functions_framework.http
def hello_http(request):
    req = request.get_json(silent=True)
    session_params = req.get('sessionInfo', {}).get('parameters', {})
    if 'transcription' in session_params:
        transcription = session_params['transcription']
    else:
        transcription = []

    if 'text' in req:
        transcription.append(req['text'])
    if 'transcript' in req:
        transcription.append(req['transcript'])

    if 'messages' in req:
        new_message = ""
        for message in req['messages']:
            new_message += message['text']['redactedText'][0]
        transcription.append(new_message)

    print(req)
    print(transcription)
    response = {
        "sessionInfo": {
            "parameters": {
                'transcription': transcription
            }
        }
    }
    return response

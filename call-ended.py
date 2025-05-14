import functions_framework
import os
from google.cloud import dialogflowcx_v3beta1 as dialogflowcx
from flask import Flask, request, jsonify

PROJECT_ID = os.environ.get('voicebot-453313')
LOCATION_ID = os.environ.get('europe-west1')
AGENT_ID = os.environ.get('fcc29f7d-81f3-432b-accd-7a07f1eba433')

@functions_framework.http
def hello_http(request):
    data = request.get_json(silent=True)

    print("XD")
    print(data)

    session_id = data.get('CallSid')
    call_status = data.get('CallStatus')
    event_name = "hangup"

    if not session_id or not event_name:
        return jsonify({"error": "session_id and event_name are required"}), 400

    session_path = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/agents/{AGENT_ID}/sessions/{session_id}"
    print("Session Path:", session_path)
    client = dialogflowcx.SessionsClient()
    event = dialogflowcx.types.EventInput(event=event_name)
    query_input = dialogflowcx.types.QueryInput(event=event)

    try:
        response = client.detect_intent(session=session_path, query_input=query_input)
        j = jsonify({
            "response": response.query_result.fulfillment_text
        }), 200
        print(j)
        return j
    except Exception as e:
        j = jsonify({"error": str(e)}), 500
        print(j)
        return j

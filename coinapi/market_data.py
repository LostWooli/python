import ssl
import websocket
import json

def on_message(ws, message):
    #print(message)
    json_data = message
    parsed_json = (json.loads(json_data))
    print(json.dumps(parsed_json.get('events')[0].get('price')))
    #print(message)

ws = websocket.WebSocketApp(
    "wss://api.gemini.com/v1/marketdata/ETHUSD",
    on_message=on_message)
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
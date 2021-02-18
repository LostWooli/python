import ssl
import websocket
import _thread as thread
import json
import jmespath

def on_message(ws, message):
    print(message)
    json_data = message
    #parsed_json = (json.loads(json_data))
    #print(json.dumps(parsed_json, indent=4, sort_keys=True))

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        ws.send(logon_msg)
    thread.start_new_thread(run, ())

if __name__ == "__main__":
    logon_msg = '{"type": "subscribe","subscriptions":[{"name":"l2","symbols":["ETHUSD"]}]}'
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://api.sandbox.gemini.com/v2/marketdata",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close,
                                on_open = on_open)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
import sys
import json
import csv
import gzip
from collections import OrderedDict
from future.moves.urllib.request import urlopen, Request
from future.moves.urllib.error import HTTPError, URLError
from future.moves.urllib.parse import urlencode



def send_webhook_request(url, body, user_agent=None):
    if url is None:
        sys.stderr.write("ERROR No URL provided\n")
        return False
    sys.stderr.write("INFO Sending POST request to url=%s with size=%d bytes payload\n" % (url, len(body)))
    sys.stderr.write("DEBUG Body: %s\n" % body)
    try:
        req = Request(url=url, data=body, headers={"Content-Type": "application/json", "User-Agent": user_agent, "Authorization": "Basic cGFnZXJwcmQ6OEglOih7RVB6bi1BNHQp"})
        sys.stderr.write("DEBUG Request: %s\n" % req)
        res = urlopen(req)
    except HTTPError as e:
        sys.stderr.write("ERROR Error sending webhook request: %s\n" % e)
    except URLError as e:
        sys.stderr.write("ERROR Error sending webhook request: %s\n" % e)
    except ValueError as e:
        sys.stderr.write("ERROR Invalid URL: %s\n" % e)
    return False


def process_event(helper, *args, **kwargs):
   # helper.log_info("Alert action critical_notify_pager911 started.")
    url = 'https://pager911.chargebacks911.com/trigger'
    user_agent = 'Splunk'
    team = helper.get_param("team")
    
    #helper.log_info("event={}".format(url))
    events = helper.get_events()
    for event in events:
        event.update({"team":team})
        #helper.log_info("event={}".format(event))
        send_webhook_request(url, json.dumps(event).encode(), user_agent=user_agent)
    
    
    
    return 0
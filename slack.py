import os
import sys
from slacksocket import SlackSocket

import urldb
import oldurl

if __name__ == '__main__':
    envs = {"token": "SLACK_TOKEN"}
    for key, env in envs.items():
        if env not in os.environ:
            print("Provide ", env, " in the environment!")
            sys.exit(1)
        envs[key] = os.environ[env]

    urldb.connect()

    s = SlackSocket(envs["token"],
                    translate=True)

    for event in s.events():
        try:
            event = event.event
            if event["type"] == "message":
                msg = oldurl.old_message(event["user"], event["text"])
                if msg:
                    sender = s.send_msg(msg,
                                        channel_name=event["channel"])
        except:
            pass

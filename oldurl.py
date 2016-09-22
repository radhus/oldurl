#!/usr/bin/env python

import sys
import re
from datetime import datetime, timedelta
import prettydate
from urltrim import trim_url
from urldb import connect, lookup_url, URL

FORMAT = ("@%(nick)s OLD! "
          "@%(found)s posted this ~%(since)s ago (%(date)s) "
          ":feelsbadman:")

# < prefix and > suffix can be added by Slack
PATTERN = re.compile(r"<?(https?://[^\s\>]+)")


def old_message(nick, text):
    args = {"nick": nick}

    match = PATTERN.findall(text)
    if not match:
        return None

    now = datetime.now()
    for url in match:
        try:
            trimmed = trim_url(url)
            find = lookup_url(trimmed)
            if find and (now - find.date) > timedelta(minutes=1):
                args["found"] = find.nick
                args["date"] = find.date.strftime("%Y-%m-%d %H:%M:%S")
                args["since"] = prettydate.pretty_datedelta(find.date, now)
                return FORMAT % args
            else:
                # store it
                u = URL(url=trimmed,
                        nick=args["nick"],
                        date=now)
                u.save()
                return None
        except:
            return None

    return None


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Need nick and text arguments")
        sys.exit(1)

    connect()

    msg = old_message(sys.argv[1], sys.argv[2])
    if msg:
        print(msg)

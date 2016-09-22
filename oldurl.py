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

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Need nick and text arguments")
        sys.exit(1)

    args = {"nick": sys.argv[1]}
    text = sys.argv[2]
    connect()

    PATTERN = re.compile(r"(https?://[^\s]+)")

    match = PATTERN.findall(text)
    if not match:
        sys.exit(0)

    now = datetime.now()
    for url in match:
        try:
            trimmed = trim_url(url)
            find = lookup_url(trimmed)
            if find and (now - find.date) > timedelta(minutes=1):
                args["found"] = find.nick
                args["date"] = find.date.strftime("%Y-%m-%d %H:%M:%S")
                args["since"] = prettydate.pretty_datedelta(find.date, now)
                print(FORMAT % args)
            else:
                # store it
                u = URL(url=trimmed,
                        nick=args["nick"],
                        date=now)
                u.save()
        except:
            sys.exit(1)

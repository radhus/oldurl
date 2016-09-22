#!/usr/bin/env python

import re
import sys
import os
from urldb import URL, lookup_url, connect
from urltrim import trim_url
from datetime import datetime


LINE_PATTERN = re.compile(r"^\[(\d+:\d+)\] <([^>]+)> (.*)$")
URL_PATTERN = re.compile(r"https?://[^ ]+")
FILENAME_PATTERN = re.compile(r".*\.([0-9]{2})([a-zA-Z]{3})([0-9]{4})$")
MONTHS = {"Jan": "01",
          "Feb": "02",
          "Mar": "03",
          "Apr": "04",
          "May": "05",
          "Jun": "06",
          "Jul": "07",
          "Aug": "08",
          "Sep": "09",
          "Oct": "10",
          "Nov": "11",
          "Dec": "12"}


def decode_line(line):
    # Check for utf-8
    try:
        line = line.decode('utf-8')
    except UnicodeDecodeError:
        line = line.decode('latin1').encode('utf-8')


def parse_line(line, datestr):
    ret = []

    line = decode_line(line)

    match = LINE_PATTERN.match(line)
    if match:
        urls = URL_PATTERN.findall(match.group(3))
        if urls:
            nick = match.group(2)
            date = datetime.strptime("%s %s" % (datestr,
                                                match.group(1)),
                                     "%Y-%m-%d %H:%M")
            for url in urls:
                if lookup_url(url):
                    continue
                try:
                    trimmed = trim_url(url)
                except:
                    continue
                u = URL(url=trimmed,
                        nick=nick,
                        date=date)
                u.save()
                ret.append(u)
    return ret


def filename_to_datestring(filename):
    fnmatch = FILENAME_PATTERN.match(filename)
    if not fnmatch:
        print("Unsupported filename:", filename)
        return None

    datestr = "%s-%s-%s" % (fnmatch.group(3),
                            MONTHS[fnmatch.group(2)],
                            fnmatch.group(1))
    return datestr


def parse_file(filename, datestr):
    ret = []

    if not os.path.isfile(filename):
        print("No such file:", filename)
        return ret

    with open(filename) as f:
        for line in f:
            try:
                ret += parse_line(line, datestr)
            except:
                print("Line unparsable:", line)

    return ret


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Need at least one filename as argument")
        sys.exit(1)

    connect()

    filenames = sys.argv[1:]
    files = dict()
    for filename in filenames:
        datestr = filename_to_datestring(filename)
        if not datestr:
            continue
        files[datestr] = filename

    for datestr in sorted(files):
        parse_file(files[datestr], datestr)

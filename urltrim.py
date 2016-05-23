from urllib import parse


def strip_www(parsed):
    if parsed.netloc[:4] != "www.":
        return parsed

    return parse.ParseResult(scheme=parsed.scheme,
                             netloc=parsed.netloc[4:],
                             path=parsed.path,
                             params=parsed.params,
                             query=parsed.query,
                             fragment=parsed.fragment)


def strip_query(parsed):
    return parse.ParseResult(scheme=parsed.scheme,
                             netloc=parsed.netloc,
                             path=parsed.path,
                             params=parsed.params,
                             query=None,
                             fragment=parsed.fragment)


def force_https(parsed):
    return parse.ParseResult(scheme="https",
                             netloc=parsed.netloc,
                             path=parsed.path,
                             params=parsed.params,
                             query=parsed.query,
                             fragment=parsed.fragment)


def trim_youtube_com(parsed):
    if parsed.path != '/watch':
        return parsed

    qs = parse.parse_qs(parsed.query)
    if 'v' not in qs:
        return parsed

    video = qs['v'][0]

    return parse.ParseResult(scheme='https',
                             netloc='youtube.com',
                             path='/watch',
                             params=None,
                             query="v=%s" % video,
                             fragment=None)


def trim_youtu_be(parsed):
    # rewrite to yotuube.com internally
    parsed = parse.ParseResult(scheme='https',
                               netloc='youtube.com',
                               path='/watch',
                               params=None,
                               query="v=%s" % parsed.path[1:],
                               fragment=None)
    return trim_youtube_com(parsed)


def trim_i_imgur(parsed):
    # should end with an image extension
    if parsed.path[-4:-3] != ".":
        return parsed
    return parse.ParseResult(scheme='http',
                             netloc='imgur.com',
                             path=parsed.path[1:-4],
                             params=None,
                             query=None,
                             fragment=None)


DOMAINS = {"youtube.com": [trim_youtube_com],
           "www.youtube.com": [strip_www,
                               trim_youtube_com],
           "youtu.be": [trim_youtu_be],
           "www.youtu.be": [strip_www,
                            trim_youtu_be],
           "reddit.com": [force_https,
                          strip_query],
           "www.reddit.com": [strip_www,
                              force_https,
                              strip_query],
           "www.aftonbladet.se": [strip_query],
           "twitter.com": [force_https,
                           strip_query],
           "www.twitter.com": [strip_www,
                               force_https,
                               strip_query],
           "i.imgur.com": [strip_query,
                           trim_i_imgur],
           "imgur.com": [strip_query],
           "www.imgur.com": [strip_www,
                             strip_query]}


def trim_url(url):
    parsed = parse.urlparse(url)
    if parsed.netloc in DOMAINS:
        for fun in DOMAINS[parsed.netloc]:
            parsed = fun(parsed)
    return parsed.geturl()

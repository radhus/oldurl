from datetime import timedelta


def pretty_timedelta(delta):
    if delta.days > 365:
        return "%d years" % round(delta.days / 365)
    if delta.days > 30:
        return "%d months" % round(delta.days / 30)
    if delta.days > 0:
        return "%d days" % delta.days

    if delta.seconds > 60 * 60:
        return "%d hours" % round(delta.seconds / (60 * 60))
    if delta.seconds > 60:
        return "%d minutes" % round(delta.seconds / 60)
    if delta.seconds > 0:
        return "%d seconds" % delta.seconds

    return "now"


def pretty_seconddelta(seconds):
    return pretty_timedelta(timedelta(0, seconds))


def pretty_datedelta(start, end):
    return pretty_timedelta(end - start)

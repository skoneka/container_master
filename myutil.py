import re
re_parser = re.compile(r'^(?P<key>\S*):\s*(?P<value>\d*)\s*kB')
def get_meminfo():
    """
    dict of data from meminfo (str:int).
    Values are in kilobytes.
    """
    result = dict()
    for line in open('/proc/meminfo'):
        match = re_parser.match(line)
        if not match:
            continue # skip lines that don't parse
        key, value = match.groups(['key', 'value'])
        result[key] = int(value)
    return result

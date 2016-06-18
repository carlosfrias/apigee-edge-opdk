#tengine server metrics

import collectd
import urllib2
import csv
import time

# Gateway Host
GATEWAY_HOST = 'localhost'

# Gateway PORT
GATEWAY_PORT = '80'

# Verbose logging on/off. Override in config by specifying 'Verbose'.
VERBOSE_LOGGING = False


def configure_callback(conf):
    """Receive configuration block"""
    global GATEWAY_HOST, GATEWAY_PORT, GATEWAY_TIMEOUT, VERBOSE_LOGGING
    for node in conf.children:
        if node.key == 'Host':
            GATEWAY_HOST = node.values[0]
        elif node.key == 'Port':
            GATEWAY_PORT = int(node.values[0])
        elif node.key == 'Timeout':
            GATEWAY_TIMEOUT = int(node.values[0])
        elif node.key == 'Verbose':
            VERBOSE_LOGGING = bool(node.values[0])
        else:
            collectd.warning('gateway_cluster plugin: Unknown config key: %s.'
                            % node.key)
    log_verbose('Configured with host=%s, port=%s, tiemout=%s, verbose_logging=%s' % (GATEWAY_HOST, GATEWAY_PORT, GATEWAY_TIMEOUT, VERBOSE_LOGGING))


def dispatch_value(info, key, type, type_instance=None):
    """Read a key from info response csv and dispatch a value"""
    value = int(info)

    type_instance = key
    cplugin = "/tengine"
    log_verbose('Sending value: %s=%s' % (type_instance, value))

    val = collectd.Values(plugin=cplugin)
    val.type = type
    val.type_instance = type_instance
    val.values = [value]
    val.dispatch()


def fetch_info():
    url = "http://" + GATEWAY_HOST + ":" + str(GATEWAY_PORT) + "/tenginestats"
    log_verbose('DEBUG: url=%s' % (url))
    try:
        time1 = time.time()
        response = urllib2.urlopen(url)
        reader = csv.reader(response)
        time2 = time.time()
    except (GATEWAY_TIMEOUT, IOError):
        time.sleep(interval)
    else:
        header = ['kv','hostip','bytes_in_total','bytes_out_total','conn_total','req_total','2xx','3xx','4xx','5xx','other','rt_total','upstream_req','upstream_rt','upstream_tries']
        rownum = 0
        for row in reader:
            xtime = (time2 * 1000 - time1 * 1000) / 1000
            colnum = 0
            for col in row:
                 if colnum == 0: #VH name
                     prefix = col;
                     #skip entry if vh name does not contain any alpha
                     if not any(c.isalpha() for c in prefix):
                         continue;
                 else:   # hostip
                     if colnum == 1:
                         prefix += col;
                     else:   # metrics
                         key = prefix + '_' + header[colnum];
                         print '%s %s' % (prefix, col)
                         log_verbose('DEBUG: %-8s: %s' % (header[colnum], col))
                         dispatch_value(col, key, 'gauge')
                 colnum += 1
            rownum += 1

def log_verbose(msg):
    if not VERBOSE_LOGGING:
        return
    collectd.info('tengine plugin [verbose]: %s' % msg)

# register callbacks
collectd.register_config(configure_callback)
collectd.register_read(fetch_info)

# Gateway cluster check

import collectd
import os
import socket
import urllib
import json
import time

# Gateway Host
GATEWAY_HOST = 'localhost'

# Gateway PORT
PORT_HOST = '8080'

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
    """Read a key from info response data and dispatch a value"""
    if key == 'responseTime':
       #value = int(float(info))
       value = float(info)
       log_verbose('DEBUG: key==responseTime value=%s' % (value))
    else:
        value = int(info)

    type_instance = "v1-cluster-" + key
    cplugin = "/gateway"
    log_verbose('Sending value: %s=%s' % (type_instance, value))

    val = collectd.Values(plugin=cplugin)
    val.type = type
    val.type_instance = type_instance
    val.values = [value]
    val.dispatch()


def fetch_info():
    url = "http://" + GATEWAY_HOST + ":" + str(GATEWAY_PORT) + "/v1/cluster"
    log_verbose('DEBUG: url=%s' % (url))
    try:
        time1 = time.time()
        conn = urllib.urlopen(url)
        data = json.loads(conn.read())
        time2 = time.time()
    except (GATEWAY_TIMEOUT, IOError):
        time.sleep(interval)
    else:
        xtime = (time2 * 1000 - time1 * 1000) / 1000
        #print "PUTVAL \"" + hostname + "/gateway/gauge-v1-cluster-memberCount\" interval="+str(interval)+" N:" + str(data['memberCount'])
        memberCount = str(data['memberCount'])
        log_verbose('DEBUG: memberCount=%s' % (memberCount))
        dispatch_value(memberCount, 'memberCount', 'gauge')

        reachableCount = str(data['reachableCount'])
        log_verbose('DEBUG: reachableCount=%s' % (reachableCount))
        dispatch_value(reachableCount, 'reachableCount', 'gauge')

        responseCode = str(conn.getcode())
        log_verbose('DEBUG: responseCode=%s' % (responseCode))
        dispatch_value(responseCode, 'responseCode', 'gauge')

        responseTime = ("%.3f" % xtime)
        log_verbose('DEBUG: responseTime=%s' % (responseTime))
        dispatch_value(responseTime, 'responseTime', 'gauge')

def log_verbose(msg):
    if not VERBOSE_LOGGING:
        return
    collectd.info('gateway_cluster plugin [verbose]: %s' % msg)

# register callbacks
collectd.register_config(configure_callback)
collectd.register_read(fetch_info)

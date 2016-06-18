# Gateway cluster check

import collectd
import os
import socket
import urllib2
import json
import time

# Gateway Host
GATEWAY_HOST = 'localhost'

# Gateway PORT
PORT_HOST = '8998'

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
            collectd.warning('gateway_heartbeat plugin: Unknown config key: %s.'
                            % node.key)
    log_verbose('Configured with host=%s, port=%s, tiemout=%s, verbose_logging=%s' % (GATEWAY_HOST, GATEWAY_PORT, GATEWAY_TIMEOUT, VERBOSE_LOGGING))


def dispatch_value(info, key, type, type_instance=None):
    """Read a key from info response data and dispatch a value"""
    if key == 'responseTime':
       value = float(info)
       log_verbose('DEBUG: key==responseTime value=%s' % (value))
    else:
        value = int(info)

    type_instance = "heartbeat-" + key
    cplugin = "/gateway"
    log_verbose('Sending value: %s=%s' % (type_instance, value))

    val = collectd.Values(plugin=cplugin)
    val.type = type
    val.type_instance = type_instance
    val.values = [value]
    val.dispatch()


def fetch_info():
    url = "http://" + GATEWAY_HOST + ":" + str(GATEWAY_PORT)
    ah = "X-Apigee.heartbeat"
    ab = "heart-beat-test"
    
    request = urllib2.Request(url)
    request.add_header(ah , ab)
    
    log_verbose('DEBUG: url=%s headers=%s:%s' % (url, ah, ab))
    try:
        time1 = time.time()
        conn = urllib2.urlopen(request)
        #conn = urllib2.urlopen(request,GATEWAY_TIMEOUT)
        time2 = time.time()
    except urllib2.URLError, e:
        log_verbose('DEBUG: %s' % (e.reason))
        responseCode = 000
        log_verbose('DEBUG: responseCode=%s' % (responseCode))
        dispatch_value(responseCode, 'responseCode', 'gauge')
        responseTime = '0.1'
        log_verbose('DEBUG: responseTime=%s' % (responseTime))
        dispatch_value(responseTime, 'responseTime', 'gauge')
        time.sleep(10)
    else:
        xtime = (time2 * 1000 - time1 * 1000) / 1000

        responseCode = conn.getcode()
        log_verbose('DEBUG: responseCode=%s' % (responseCode))
        dispatch_value(responseCode, 'responseCode', 'gauge')

        responseTime = ("%.3f" % xtime)
        log_verbose('DEBUG: responseTime=%s' % (responseTime))
        dispatch_value(responseTime, 'responseTime', 'gauge')

def log_verbose(msg):
    if not VERBOSE_LOGGING:
        return
    collectd.info('gateway_heartbeat plugin [verbose]: %s' % msg)

# register callbacks
collectd.register_config(configure_callback)
collectd.register_read(fetch_info)


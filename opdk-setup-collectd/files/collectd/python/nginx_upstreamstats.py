# nginx/tengine /upstreamstats

import collectd
import urllib2
import json
import socket

# Gateway Host
GATEWAY_HOST = '127.0.0.1'

# Gateway PORT
GATEWAY_PORT = '9000'

# Gateway timeout
GATEWAY_TIMEOUT = 20

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
            collectd.warning('nginx_upstreamstats plugin: Unknown config key: %s.'
                            % node.key)
    log_verbose('Configured with host=%s, port=%s, tiemout=%s, verbose_logging=%s' % (GATEWAY_HOST, GATEWAY_PORT, GATEWAY_TIMEOUT, VERBOSE_LOGGING))


def dispatch_value(value, type_instance, type):
    """Read a key from info response csv and dispatch a value"""
    value = int(value)

    log_verbose('Sending value: %s=%s' % (type_instance, value))

    val = collectd.Values(plugin='/nginx', plugin_instance='upstreamstats')
    val.type = type
    val.type_instance = type_instance
    val.values = [value]
    val.dispatch()


def fetch_info():
    url = 'http://{}:{}/upstreamstats'.format(GATEWAY_HOST, GATEWAY_PORT)

    try:
        response = urllib2.urlopen(url, timeout=GATEWAY_TIMEOUT)
        upstream_stats = json.load(response)
    except urllib2.URLError as e:
        raise
    except socket.timeout as e:
        raise Exception('Socket timeout: %r' % e)
    else:
        for vhost, counts_by_status_code in upstream_stats.items():
            for status_code, count in counts_by_status_code.items():
                key = '{}_{}'.format(vhost, status_code)
                dispatch_value(count, key, 'gauge')


def log_verbose(msg):
    if not VERBOSE_LOGGING:
        return
    collectd.info('nginx_upstreamstats plugin [verbose]: %s' % msg)

# register callbacks
collectd.register_config(configure_callback)
collectd.register_read(fetch_info)

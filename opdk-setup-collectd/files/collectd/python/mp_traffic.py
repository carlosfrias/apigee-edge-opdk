# mp_traffic server metrics

import collectd
import json
import time
import urllib2

# Gateway Host
GATEWAY_HOST = 'localhost'

# Gateway PORT
GATEWAY_PORT = '80'

# Verbose logging on/off. Override in config by specifying 'Verbose'.
VERBOSE_LOGGING = True

GATEWAY_TIMEOUT = 10


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
    log_verbose('Configured with host=%s, port=%s, tiemout=%s, verbose_logging=%s' % (
        GATEWAY_HOST, GATEWAY_PORT, GATEWAY_TIMEOUT, VERBOSE_LOGGING))


def dispatch_value(info, key, type, type_instance=None):
    """Read a key from info response csv and dispatch a value"""
    value = int(info)

    type_instance = key
    cplugin = "/mp_traffic"
    log_verbose('Sending value: %s=%s' % (type_instance, value))

    val = collectd.Values(plugin=cplugin)
    val.type = type
    val.type_instance = type_instance
    val.values = [value]
    val.dispatch()


def fetch_info():
    url = 'http://%(host)s:%(port)s/v1/server/metrics' % {'host': GATEWAY_HOST, 'port': GATEWAY_PORT}
    log_verbose('DEBUG: url=%s' % (url))
    try:
        time1 = time.time()
        response = urllib2.urlopen(url)
        traffic = json.load(response)
        time2 = time.time()
        # log_verbose('DEBUG: traffic=%s' % (traffic))
    except (IOError):
        time.sleep(GATEWAY_TIMEOUT)
    else:
        inbound_request_count = 0
        client_responses_2xx = 0
        client_responses_4xx = 0
        client_responses_5xx = 0
        total_samples = 0
        total_time = 0

        for counter in traffic['inboundTraffic']:
            total_samples += counter['endToEndLatency']['totalSamples']
            total_time += counter['endToEndLatency']['totalSamples'] * counter['endToEndLatency']['average']
            inbound_request_count += counter['requestsReceived']['total']
            for responseByCode in counter['responsesSent']['responseByCode']:
                if responseByCode['type'].startswith('2'):
                    client_responses_2xx += responseByCode['count']
                if responseByCode['type'].startswith('4'):
                    client_responses_4xx += responseByCode['count']
                if responseByCode['type'].startswith('5'):
                    client_responses_5xx += responseByCode['count']

        if total_samples:
            average_latency_mp = total_time / total_samples
        else:
            average_latency_mp = 0

        dispatch_value(inbound_request_count, 'cumulative-requestsReceived', 'gauge')
        dispatch_value(client_responses_2xx, 'cumulative-responsesSent2xx', 'gauge')
        dispatch_value(client_responses_4xx, 'cumulative-responsesSent4xx', 'gauge')
        dispatch_value(client_responses_5xx, 'cumulative-responsesSent5xx', 'gauge')
        dispatch_value(average_latency_mp, 'cumulative-averageRequestLatency', 'gauge')
        total_samples = 0
        total_time = 0
        target_request_count = 0
        target_responses_2xx = 0
        target_responses_4xx = 0
        target_responses_5xx = 0

        for counter in traffic['outboundTraffic']:
            total_samples += counter['roundTripTime']['totalSamples']
            total_time += counter['roundTripTime']['totalSamples'] * counter['roundTripTime']['average']
            target_request_count += counter['requestsSent']['total']
            for responseByCode in counter['responsesReceived']['responseByCode']:
                if responseByCode['type'].startswith('2'):
                    target_responses_2xx += responseByCode['count']
                if responseByCode['type'].startswith('4'):
                    target_responses_4xx += responseByCode['count']
                if responseByCode['type'].startswith('5'):
                    target_responses_5xx += responseByCode['count']
        if total_samples:
            average_latency_target = total_time / total_samples
        else:
            average_latency_target = 0

        dispatch_value(target_request_count, 'cumulative-requestsSentToTarget', 'gauge')
        dispatch_value(target_responses_2xx, 'cumulative-responsesFromTarget2xx', 'gauge')
        dispatch_value(target_responses_2xx, 'cumulative-responsesFromTarget4xx', 'gauge')
        dispatch_value(target_responses_2xx, 'cumulative-responsesFromTarget5xx', 'gauge')
        dispatch_value(average_latency_target, 'cumulative-averageTargetLatency', 'gauge')


def log_verbose(msg):
    if not VERBOSE_LOGGING:
        return
    collectd.info('mptraffic plugin [verbose]: %s' % msg)


# register callbacks
collectd.register_config(configure_callback)
collectd.register_read(fetch_info)

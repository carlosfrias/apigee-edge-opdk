# Memory and CPU Load stats

from __future__ import division
import collectd

import socket
import os
import multiprocessing

import time
import psutil
from psutil._compat import print_


def configure_callback(conf):
    """Receive configuration block"""
    global VERBOSE_LOGGING
    for node in conf.children:
        if node.key == 'Verbose':
            VERBOSE_LOGGING = bool(node.values[0])
        else:
            collectd.warning('memory_load_stats plugin: Unknown config key: %s.'
                            % node.key)
    log_verbose('RUNNING memory_load_stats, verbose_logging=%s' % VERBOSE_LOGGING)


def dispatch_value(info, key, type, cplugin=collectd):
    """Read a key from info response data and dispatch a value"""
    #value = info
    value = float(info)
    type_instance = key
    log_verbose('Sending value: %s=%s' % (type_instance, value))

    val = collectd.Values(plugin=cplugin)
    val.type = type
    val.type_instance = type_instance
    val.values = [value]
    val.dispatch()


def fetch_info():
    #get memory usage
    mem = psutil.virtual_memory()
    avail_buffers_cached = (mem.buffers + mem.cached)
    
    percent_used = mem.percent
    percent_used_bc = (mem.total / avail_buffers_cached) / mem.total * 100

    log_verbose('DEBUG: percent_used=%s' % (percent_used))
    dispatch_value(percent_used, 'percent_used', 'gauge', 'memory')
    log_verbose('DEBUG: percent_used_bc=%s' % (percent_used_bc))
    dispatch_value(percent_used_bc, 'percent_used_bc', 'gauge', 'memory')

    #get normalized load
    load_avg = os.getloadavg()[0]
    num_cpu = multiprocessing.cpu_count()
    normalized_load = ( load_avg / num_cpu)

    log_verbose('DEBUG: normalized_load=%.2f' % (normalized_load))
    dispatch_value(normalized_load, 'shortterm_per_cpu', 'gauge', '/load')

    #sleep to let CPU settle
    time.sleep(1)

    #get cpu percent usage
    cpu_percent = psutil.cpu_percent(1)

    log_verbose('DEBUG: cpu_percent_used=%.2f' % (cpu_percent))
    dispatch_value(cpu_percent, 'cpu_percent_used', 'gauge', 'cpu')

def log_verbose(msg):
    if not VERBOSE_LOGGING:
        return
    collectd.info('memory_load_stats plugin [verbose]: %s' % msg)

# register callbacks
collectd.register_config(configure_callback)
collectd.register_read(fetch_info)

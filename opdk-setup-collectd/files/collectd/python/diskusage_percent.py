# Disk Usage by Percent

import collectd
import os
import socket

# Disk Host
DISK_HOST = 'localhost'

# Verbose logging on/off. Override in config by specifying 'Verbose'.
VERBOSE_LOGGING = False

ignorefs = set(["rootfs","mqueue","debugfs","tmpfs","devtmpfs","proc","sysfs","securityfs","devpts","cgroup","autofs","hugetlbfs","configfs","fusectl","binfmt_misc","fuse.gvfsd-fuse"])


def get_fs_freespace(pathname):
    stat = os.statvfs(pathname)
    log_verbose('DEBUG: pathname=%s' % (pathname))
    if stat.f_blocks>0:
        return (stat.f_blocks - stat.f_bavail) / (stat.f_blocks / 100)
    else:
        return -1

def configure_callback(conf):
    """Receive configuration block"""
    global DISK_HOST, VERBOSE_LOGGING
    for node in conf.children:
        if node.key == 'Host':
            DISK_HOST = node.values[0]
        elif node.key == 'Verbose':
            VERBOSE_LOGGING = bool(node.values[0])
        else:
            collectd.warning('diskusage_percent plugin: Unknown config key: %s.'
                            % node.key)
    log_verbose('Configured with host=%s, verbose_logging=%s' % (DISK_HOST, VERBOSE_LOGGING))


def dispatch_value(info, key, type, type_instance=None):
    """Read a key from info response data and dispatch a value"""
    value = int(info)
    #type_instance = "/disk" + key + "/percent_bytes-used" 
    type_instance = "percent_bytes-used" 
    cplugin = "/disk" + key
    log_verbose('Sending value: %s=%s' % (type_instance, value))

    val = collectd.Values(plugin=cplugin)
    val.type = type
    val.type_instance = type_instance
    val.values = [value]
    val.dispatch()


def fetch_info():
   with open('/etc/mtab') as f:
     content = f.readlines()
   
   myset = set()
   
   for line in content:
     sp = line.split()
     if sp[2] not in ignorefs:
         myset.add (sp[1])
         log_verbose('DEBUG: line=%s' % (line))
   for line in myset:
     log_verbose('DEBUG: find percent used for %s' % (line))
     freespace = str(get_fs_freespace(line))
     if line == "/":
         line = "-root"
     line = line.replace("/","-")
     #print "PUTVAL \"" + hostname + "/disk" + line + "/percent_bytes-used" + "\" interval=" + str(interval) + " N:" + freespace
     log_verbose('DEBUG: found %s for %s' % (freespace, line))
     dispatch_value(freespace, line, 'gauge')
   
def log_verbose(msg):
    if not VERBOSE_LOGGING:
        return
    collectd.info('diskusage_percent plugin [verbose]: %s' % msg)

# register callbacks
collectd.register_config(configure_callback)
collectd.register_read(fetch_info)

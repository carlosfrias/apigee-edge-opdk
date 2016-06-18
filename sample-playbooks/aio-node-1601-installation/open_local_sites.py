#! /usr/bin/python

from subprocess import call

local_sites = [
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8080/v1/servers',
    'http://127.0.0.1:9000',
    'http://127.0.0.1:9090',
    'http://127.0.0.1:8081/v1/server/metrics',
    'http://127.0.0.1:8081/v1/server/metrics/inbound/traffic',
]

for site in local_sites:
    print("Opening: {}".format(site))
    call(['open', site])

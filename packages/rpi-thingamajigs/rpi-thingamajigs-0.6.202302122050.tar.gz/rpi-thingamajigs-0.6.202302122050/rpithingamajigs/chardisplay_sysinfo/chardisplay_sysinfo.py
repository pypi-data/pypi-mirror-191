import humanize
from datetime import datetime
import socket
import psutil
import os
from time import sleep
from rpithingamajigs.lcdd.client import LcddClient

def sysinfo_hostname():
    hostname = socket.gethostname()
    return hostname

def sysinfo_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        address = s.getsockname()[0]
    except:
        address = '127.0.0.1'
    finally:
        s.close()
    return address

def sysinfo_uptime():
    uptime = humanize.naturaldelta(datetime.now() - datetime.fromtimestamp(psutil.boot_time()))
    return uptime

def queue_messages(client, duration = 6):
    mem = psutil.virtual_memory()
    load = os.getloadavg()
    hostname = sysinfo_hostname()
    uptime = sysinfo_uptime()
    address = sysinfo_ip_address()

    client.message( [
        'host: {}'.format(hostname),
        '  ip: {}'.format(address),
        'load: {:.2f} (1min)'.format(load[0]),
        ' mem: {} used'.format(humanize.naturalsize(mem.used))
        ], duration)

    client.message( [
        'host: {}'.format(hostname),
        '  up: {}'.format(address),
        'load: {:.2f} (5min)'.format(load[1]),
        ' mem: {} total'.format(humanize.naturalsize(mem.total))
        ], duration)

    client.message( [
        'host: {}'.format(hostname),
        '  up: {}'.format(uptime),
        'load: {:.2f} (15min)'.format(load[2]),
        ' mem: {}% used'.format(mem.percent)
        ], duration)

if __name__ == '__main__':
    client = LcddClient()
    client.connect(True)
    cadence = 60
    while True:
        queue_messages(client, cadence + 5)
        sleep(cadence)

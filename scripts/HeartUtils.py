### Python 3.6.8 does not have a nanosecond time function. I hate Python.
### With Python, everything is alwasys "in some later version than the one
### that you are using". Well, except for threads.
###
import subprocess
import time
import re
import os
from multiprocessing import Process, Queue
import sys
import traceback

##
## For multiprocess. Read from a queue and send checks to InfluxDB.
##
def statsWriter (q, url, db):
    while True:
        d = q.get()
        try:
            writeStats(url, db, d['ok'], d['now'], d['latency'], d['beatDiff'], d['beat'])
        except Exception as e:
            print("writeStats failed:\n", e)
            traceback.print_exc()
        if d['end']:
            sys.exit(0)

##
## For multiprocess. Read from a queue and send checks to Icinga.
##
def checkWriter (q, url, sn):
    while True:
        d = q.get()
        try:
            writeCheck(url, sn, d['ok'], d['now'], d['latency'], d['beatDiff'])
        except:
            print("writeCheck failed:\n", e)
            traceback.print_exc()
        if d['end']:
            sys.exit(0)

def writeStats (url, db, ok, now, latency, beatDiff, beat):
    if (ok == 1):
        command = "curl --connect-timeout 10 -m 20  -sk -XPOST '%s/write?db=%s' -u $INFLUX_CREDS --data-binary \"hearbeat ok=%d,latency=%f,beatdiff=%d,beat=%d %d\"" % (url, db, ok, latency, beatDiff, beat, now)
    else:
        command = "curl --connect-timeout 10 -m 20  -sk -XPOST '%s/write?db=%s' -u $INFLUX_CREDS --data-binary \"hearbeat ok=%d %d\"" % (url, db, ok, now)
    proc = subprocess.run([command], shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, timeout=20)
    iout = proc.stdout.decode().splitlines()
    ierr = proc.stderr.decode().splitlines()
    if (proc.returncode != 0):
        print("============================")
        print("Error talking to influx.")
        print("============================")
        print(proc.stdout.decode().splitlines())
        print("============================")
        print(proc.stderr.decode().splitlines())
        print("============================")

def writeCheck (url, sn, ok, now, latency, beatDiff):
   if (os.environ.get('ICINGA_CHECK_HOST')):
      check_host = os.environ['ICINGA_CHECK_HOST']
   else:
      return
   if (ok == 1):
     prefix = "OK"
     state  = 0
     if (latency > 10):
       prefix = "CRITICAL"
       state  = 2
     elif (latency > 2):
       prefix = "WARNING"
       state = 1
     message = prefix + ": " + "latency: %f" % latency
     command = "curl --connect-timeout 10 -m 20 -sk -XPOST -u $ICINGA_CREDS -H  'Accept: application/json' -H 'Content-type: application/json'  '%s' -d '{\"type\":\"Service\", \"filter\":\"host.name==\\\"%s\\\" && service.name==\\\"%s\\\"\", \"exit_status\": %d, \"plugin_output\": \"%s\", \"performance_data\": [ \"latency=%f;\" ], \"check_source\": \"hopbeat_monitor\"}'" % (url, check_host, sn, state, message, latency)
   else:
     message = "UNKNOWN: hop timeout"
     command = "curl --connect-timeout 10 -m 20 -sk -XPOST -u $ICINGA_CREDS -H  'Accept: application/json' -H 'Content-type: application/json'  '%s' -d '{\"type\":\"Service\", \"filter\":\"host.name==\\\"%s\\\" && service.name==\\\"%s\\\"\", \"exit_status\": %d, \"plugin_output\": \"%s\", \"check_source\": \"hopbeat_monitor\"}'" % (url, check_host, sn, 3, message)
   proc = subprocess.run([command], shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, timeout=20)
   iout = proc.stdout.decode().splitlines()
   ierr = proc.stderr.decode().splitlines()
   if (proc.returncode != 0):
        print("============================")
        print("Error talking to icinga.")
        print("============================")
        print(proc.stdout.decode().splitlines())
        print("============================")
        print(proc.stderr.decode().splitlines())
        print("============================")

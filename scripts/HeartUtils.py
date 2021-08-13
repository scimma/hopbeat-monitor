### Python 3.6.8 does not have a nanosecond time function. I hate Python.
### With Python, everything is alwasys "in some later version than the one
### that you are using". Well, except for threads.
###
import subprocess
import time
import re
import os

def writeStats (url, db, ok, now, latency, beatDiff):
    if (ok == 1):
        command = "curl -sk -XPOST '%s/write?db=%s' -u $INFLUX_CREDS --data-binary \"hearbeat ok=%d,latency=%f,beatdiff=%d %d\"" % (url, db, ok, latency, beatDiff, now)
    else:
        command = "curl -sk -XPOST '%s/write?db=%s' -u $INFLUX_CREDS --data-binary \"hearbeat ok=%d %d\"" % (url, db, ok, now)
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
   elif (beats > 2):
       prefix = "WARNING"
       state = 1
     message = prefix + ": " + "latency: %f" % latency
     command = "curl -sk -XPOST -u $ICINGA_CREDS -H  'Accept: application/json' -H 'Content-type: application/json'  '%s' -d '{\"type\":\"Service\", \"filter\":\"host.name==\\\"%s\\\" && service.name==\\\"%s\\\"\", \"exit_status\": %d, \"plugin_output\": \"%s\", \"performance_data\": [ \"bpm=%d;\" ], \"check_source\": \"hopbeat_monitor\"}'" % (url, check_host, sn, state, message, beats)
   else:
     message = "UNKNOWN: hop timeout"
     command = "curl -sk -XPOST -u $ICINGA_CREDS -H  'Accept: application/json' -H 'Content-type: application/json'  '%s' -d '{\"type\":\"Service\", \"filter\":\"host.name==\\\"%s\\\" && service.name==\\\"%s\\\"\", \"exit_status\": %d, \"plugin_output\": \"%s\", \"check_source\": \"hopbeat_monitor\"}'" % (url, check_host, sn, state, message)
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


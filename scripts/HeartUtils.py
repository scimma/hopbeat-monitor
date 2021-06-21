### Python 3.6.8 does not have a nanosecond time function. I hate Python.
### With Python, everything is alwasys "in some later version than the one
### that you are using". Well, except for threads.
###
import subprocess
import time
import re
import os

def getStats (url, topic):
    command = "/usr/local/bin/kafkacat -F /root/share/kafkacat.conf -b %s -C -t %s -o -1 -e " % (url, topic)
#    startTime = time.time_ns()
    startTime = int(time.time() * 10**9)

    try:
        proc = subprocess.run([command], shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE, timeout=20)
    except subprocess.TimeoutExpired:
        return [0, 0, 0.0, 0, 0]

    lines = proc.stdout.decode().splitlines()
    endTimeFloat   = time.time()
    endTime        = int(endTimeFloat * 10**9)
#    endTime = time.time_ns()
    endTimeMicroSeconds = int(endTimeFloat * 10**6)
    latestBeatTime = 0
    latestBeat     = 0
    for line in lines:
        m = re.match('^.*{\"timestamp\":\s+([0-9]+),\s+\"count\":\s+([0-9]+),', line)
        if m != None:
            curTime = int(m.group(1)) # in microseconds
            curBeat = int(m.group(2))
            if (curTime > latestBeatTime):
                latestBeatTime = curTime
                latestBeat     = curBeat
    return [1, endTime, (endTime - startTime)/float(10**9), latestBeat, endTimeMicroSeconds - latestBeatTime]

def writeStats (url, db, ok, now, ktime, lb, cb, bl):
    if (ok == 1):
        command = "curl -sk -XPOST '%s/write?db=%s' -u $INFLUX_CREDS --data-binary \"hearbeat ok=%d,commtime=%f,beats=%d,beatlag=%d %d\"" % (url, db, ok, ktime, cb - lb, bl, now)
    else:
        command = "curl -sk -XPOST '%s/write?db=%s' -u $INFLUX_CREDS --data-binary \"hearbeat ok=%d\"" % (url, db, ok)
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

def writeCheck (url, sn, ok, now, ktime, lb, cb, bl):
   beats = cb - lb
   if (os.environ.get('ICINGA_CHECK_HOST')):
      check_host = os.environ['ICINGA_CHECK_HOST']
   else:
      return
   if (ok == 1):
     prefix = "OK"
     state  = 0
     if (beats < 40):
       prefix = "CRITICAL"
       state  = 2
     elif (beats < 55):
       prefix = "WARNING"
       state = 1
     message = prefix + ": " + "beats: %d" % beats
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

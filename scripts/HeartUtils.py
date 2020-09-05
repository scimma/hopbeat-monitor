### Python 3.6.8 does not have a nanosecond time function. I hate Python.
### With Python, everything is alwasys "in some later version than the one
### that you are using". Well, except for threads.
###
import subprocess
import time
import re

def getStats (url):
    command = "/usr/local/bin/kafkacat -F /root/share/kafkacat.conf -b %s -C -t heartbeat -o -1 -e " % url
#    startTime = time.time_ns()
    startTime = int(time.time() * 1000000000)

    try:
        proc = subprocess.run([command], shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE, timeout=20)
    except subprocess.TimeoutExpired:
        return [0, 0, 0.0, 0, 0]

    lines = proc.stdout.decode().splitlines()
    endTimeFloat   = time.time()
    endTime        = int(endTimeFloat * 1000000000)
#    endTime = time.time_ns()
    endTimeSeconds = int(endTimeFloat)
    latestBeatTime = 0
    latestBeat     = 0
    for line in lines:
        m = re.match('^\s*{\"timestamp\":\s+([0-9]+),\s+\"count\":\s+([0-9]+),', line)
        if m != None:
            curTime = int(m.group(1))
            curBeat = int(m.group(2))
            if (curTime > latestBeatTime):
                latestBeatTime = curTime
                latestBeat     = curBeat
    return [1, endTime, (endTime - startTime)/1000000000.0, latestBeat, endTimeSeconds - latestBeatTime]

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

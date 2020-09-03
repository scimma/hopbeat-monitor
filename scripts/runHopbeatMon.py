#!/usr/bin/python3
###
### Author: rdt12@psu.edu
### Date:   Apr 24, 2020
### Desc:   Run gcn2hop in a loop with credentials taken from an AWS secret.
###
from datetime import datetime, timezone
import Utils as u
import time
import pytz
import sys
import os

region    = "us-west-2"
secret    = "dev-gcn2hop-hopcreds"
configDir = "/root/share"
Location  = "%s/kafkacat.conf" % configDir
hopUrl    = "kafka://dev.hop.scimma.org:9092/heartbeat"

## Line buffer stdout and stderr
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)

os.system("mkdir -p %s" % configDir)
creds  = u.getCreds(region, secret)
u.writeConfig(Location, creds)

while True:
    print("======================================")
    print("== Starting hopbeatMon")
    print("Date: %s" % datetime.now(pytz.timezone('America/New_York')))
    print("======================================")
    exitVal = os.system("/root/hopbeatMon -F %s --scimma=%s" % (Location, hopUrl))
    print("hopbeatMon exited with os.system returning: %d" % exitVal)
    time.sleep(30)

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

region       = "us-west-2"
hopSecret    = "dev-gcn2hop-hopcreds"
influxSecret = "dev-influxdb-hop-writer-creds" 
configDir    = "/root/share"
Location     = "%s/kafkacat.conf" % configDir
hopUrl       = "dev.hop.scimma.org:9092"

## Line buffer stdout and stderr
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)

os.system("mkdir -p %s" % configDir)
hopCreds    = u.getCreds(region, hopSecret)
influxCreds = u.getCredsString(region, influxSecret)
u.writeConfig(Location, hopCreds)
os.environ["INFLUX_CREDS"] = influxCreds

while True:
    print("======================================")
    print("== Starting hopbeatMon")
    print("Date: %s" % datetime.now(pytz.timezone('America/New_York')))
    print("======================================")
    exitVal = os.system("/root/hopbeatMon -F %s --scimma=%s" % (Location, hopUrl))
    print("hopbeatMon exited with os.system returning: %d" % exitVal)
    time.sleep(30)

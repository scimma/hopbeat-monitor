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
icingaSecret = "icinga-api-creds"
configDir    = "/root/shared"
Location     = "%s/config.toml" % configDir
hopUrl       = "dev.hop.scimma.org:9092"
interval     = "60"

if (os.environ.get('HOP_URL') is not None):
    hopUrl = os.environ.get('HOP_URL')

if (os.environ.get('HOP_SECRET') is not None):
    hopSecret = os.environ.get('HOP_SECRET')

if (os.environ.get('HOP_REGION') is not None):
    region = os.environ.get('HOP_REGION')

if (os.environ.get('INFLUX_SECRET') is not None):
    influxSecret = os.environ.get('INFLUX_SECRET')

if (os.environ.get('ICINGA_SECRET') is not None):
    icingaSecret = os.environ.get('ICINGA_SECRET')

if (os.environ.get('MONITOR_INTERVAL') is not None):
    interval = os.environ.get('MONITOR_INTERVAL')

if (os.environ.get('HOP_CREDS') is not None):
    hopCreds = u.getCredsFromString(os.environ.get('HOP_CREDS'))
else:
    hopCreds = u.getCreds(region, hopSecret)

if (os.environ.get('INFLUX_CREDS') is not None):
   influxCreds = os.environ.get('INFLUX_CREDS')
else:
   influxCreds = u.getCredsString(region, influxSecret)
   os.environ["INFLUX_CREDS"] = influxCreds

if (os.environ.get('ICINGA_CREDS') is not None):
   icingaCreds = os.environ.get('ICINGA_CREDS')
else:
   icingaCreds = u.getSecret(region, icingaSecret)   
   os.environ["ICINGA_CREDS"] = icingaCreds

## Line buffer stdout and stderr
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)

os.system("mkdir -p %s" % configDir)
u.writeConfig(Location, hopCreds)

while True:
    print("======================================")
    print("== Starting hopbeatMon")
    print("Date: %s" % datetime.now(pytz.timezone('America/New_York')))
    print("======================================")
    exitVal = os.system("/root/hopbeatMon -F %s --scimma=%s" % (Location, hopUrl))
    print("hopbeatMon exited with os.system returning: %d" % exitVal)
    time.sleep(int(interval))

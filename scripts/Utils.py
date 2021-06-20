###
### Author: rdt12@psu.edu
### Date:   Jun 29, 2020
### Desc:   Utility functions for runGcn2Hop.py
###
import json
import subprocess
import re
from hop import models
from hop import publish
from hop import io

def getCreds (region, secret):
  cmd   = "/usr/local/bin/aws --region %s secretsmanager get-secret-value --secret-id %s" % (region, secret)
  s = json.loads(subprocess.Popen([cmd], shell=True,
                             stdout=subprocess.PIPE).stdout.read().decode())
  cjson = s["SecretString"]
  c = json.loads(cjson)
  cm = re.match(r'^([^:]+):(.*)$', c["creds"])
  if cm != None:
      creds = {"user": cm.group(1), "pass": cm.group(2)}
  else:
      creds = None
  return creds

def getCredsString (region, secret):
  cmd   = "/usr/local/bin/aws --region %s secretsmanager get-secret-value --secret-id %s" % (region, secret)
  s = json.loads(subprocess.Popen([cmd], shell=True,
                             stdout=subprocess.PIPE).stdout.read().decode())
  cjson = s["SecretString"]
  c = json.loads(cjson)
  return c["creds"]

def getSecret (region, secret) {
  cmd   = "/usr/local/bin/aws --region %s secretsmanager get-secret-value --secret-id %s" % (region, secret)
  s = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE).stdout.read().decode()
  return s
}

def writeConfig (loc, creds):
    cfh = open(loc, "w")
    cfh.write("security.protocol=SASL_SSL\n")
    cfh.write("sasl.username=%s\n" % creds["user"])
    cfh.write("sasl.password=%s\n" % creds["pass"])
    cfh.write("sasl.mechanism=SCRAM-SHA-512\nssl.ca.location=/etc/pki/tls/certs/ca-bundle.trust.crt\n")
    cfh.close()

class ScimmaConnection:

    def __init__ (self, scimmaUrl, scimmaConfFile):
        self.scimmaUrl      = scimmaUrl
        self.scimmaConfFile = scimmaConfFile
        self.msgCount       = 0

    def open (self):
        self.stream       = io.Stream(config=self.scimmaConfFile, format="json")
        self.streamHandle = self.stream.open(self.scimmaUrl, mode="w", format="json")

    def write (self, msg):
        self.streamHandle.write(msg)
        self.msgCount = self.msgCount + 1
        print("Sent message %d" % self.msgCount)

    def close (self):
        self.streamHandle.close()


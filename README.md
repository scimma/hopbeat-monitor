# hopbeat-monitor container

This repository is used to buiild a container for 
a simple HOP-based applet that reads from a topic
and reports statistics. In particular it reads
from the heartbeat topic on the HOP kafka server.

## Environment

* HOP_URL          - Hop server URL. Default: "dev.hop.scimma.org:9092".
* HOP_TOPIC        - Topic to read heartbeats. Default: "heartbeat".
* HOP_SECRET       - AWS Secret containing credentials for reading HOP_TOPIC stored in the form: Key=creds Value=USER:PASS.
* HOP_REGION       - AWS REGION where secrets are stored. Default: "us-west-2"
* INFLUX_URL       - URL of Influx Server. Default: "http://influx.dev.hop.scimma.org:8010".
* INFLUX_DB        - INFLUX DB to which to write metrics. Default: "hop".
* INFLUX_SECRET    - AWS Secret containing credentials for writing INLFUX stored in the form: Key=creds Value=USER:PASS.
* MONITOR_INTERVAL - Time interval in seconds between metric collections.

## Metrics

Grafana calls the value of INFLUX_DB a *measurement*. Grafana calls the metrics *fields*.

The metrics that are reported every MONITOR_INTERVAL:

* ok - 1 if communication with HOP was successful, zero otherwise.
* commtime - The floating point time in seconds spent talking to the HOP server.
* beats    - The number of beats since the last metric collection time (MONITOR_INTERVAL).
* beatlag  - The time between the send time of the latest beat and the time that it was received. This is _not_ a performance metric. Numbers less than the time between beat writes depends on chance and the rate at which beats are read. However a beatlag greater than the interval at which beats are normally written is unexpected and could indicate a problem either with HOP or the hopbeat monitoring system.

## Build

```
make 
```

## Release

Pushing to AWS ECR is handled via a github workflow. To push a container based on
the current master branch to AWS ECR with
version MAJOR.MINOR.RELEASE (e.g., "0.0.7") do:

```
git tag version-MAJOR.MINOR.RELEASE
git push origin version-MAJOR.MINOR.RELEASE
```

## TODO


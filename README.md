# hopbeat-monitor container

This repository is used to buiild a container for 
a simple HOP-based applet that reads from a topic
and reports statistics. In particular it reads
from the heartbeat topic on the HOP kafka server.

## Build

```
make 
```

## Push to Amazon ECS

This should only be done via github CI.

```
make push
```

## TODO

1. setup github CI
2. modify the makefile to use environment variables from github CI to determine the versions/tags for pushing to AWS ECR.
3. ``runHopBeatMon.py`` could be made more robust.

# hopbeat-monitor container

This repository is used to buiild a container for 
a simple HOP-based applet that reads from a topic
and reports statistics. In particular it reads
from the heartbeat topic on the HOP kafka server.

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


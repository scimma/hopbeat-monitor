## Dec 6, 2022 - version 1.1.1

  1. Remove metrics associated with Icinga and InfluxDB communication.

  2. Move Icinga and InfluxDB communication to a separate process.

## Sep 22, 2022 - version 1.0.14

  1. Add additional metrics to quantify time spent communicating with Icinga and InfluxDB.

  2. Try to account for the time.

## Sep 30, 2021 - version 0.0.21

  1. Update to scimma/client:0.5.3

## Nov 25, 2020 - version 0.0.12

  1. Github CI has been configured so that the container is built
     for non-master pushes and deployed for version tags.

  2. Release version is now derived from GITHUB_REF variable.

  3. Removed bin/awsDockerLogin.

timewarp.py

Given a list of Junos device IPs, timewarp will set the Timezone and an NTP server, then commit the configuration and synchronise the clock source (```set date ntp```) using the Junos REST API.

Requires Junos 15.1R1.8 or later, and:

```set system services rest http port 8080```

configured on the router.

The python lib ```requests``` is also required.

```
$ ./timwarp.py hostlist

Timewarp

Username: root
Password: *******
Applied Timezone Configuration to 10.0.0.81
Applied NTP Configuration to 10.0.0.81
Committed configuration to 10.0.0.81
Synchronised NTP on node 10.0.0.81

Applied Timezone Configuration to 10.0.0.82
Applied NTP Configuration to 10.0.0.82
Committed configuration to 10.0.0.82
Synchronised NTP on node 10.0.0.82

```
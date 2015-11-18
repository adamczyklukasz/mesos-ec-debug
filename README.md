# Mesos Agent/Slave with External Containerizer ignores mesos.internal.RunTaskMessage

I have odd problem with Mesos Agent + External Containerizer: I'm able to schedule only 14 tasks per agent (sic!), after reaching that limit my mesos-agent ignores mesos.internal.RunTaskMessage from mesos-master.

## Provisioning
```
vagrant up
```
> Default configuration: 1 x mesos-master (1CPU, 512MB) + 1 x mesos-slave (1CPU, 1GB)

## Mesos Master WebUI

http://192.168.255.10:5050

## Marathon WebUI

http://192.168.255.10:8080

## Steps to reproduce problem

```
curl -X POST -H "Content-Type: application/json" http://192.168.255.10:8080/v2/apps -d '
{
    "id": "sleep",
    "cmd": "sleep 1000000",
    "instances": 2,
    "cpus": 0.1,
    "mem": 16
}'
```

1. Add task

2. Check Mesos-master console: http://192.168.255.10:5050 Should work fine.

3. Scale up to 16+ instances (per node)

4. See how Mesos-slave will die :(

More details: http://www.mail-archive.com/dev@mesos.apache.org/msg33484.html

Simplest External Containerizer Program: https://github.com/klocekPL/mesos-ec-debug/blob/master/ecp/ecp.py

Real life example: https://github.com/AVSystem/mesoslxc

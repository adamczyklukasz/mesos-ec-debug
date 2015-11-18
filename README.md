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

* Add task

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
* Check Mesos-master console: http://192.168.255.10:5050 Should work fine.

* Scale up to 15+ instances (per node)

```
curl -X PUT -H "Content-Type: application/json" http://192.168.255.10:8080/v2/apps/sleep -d '
{
    "instances": "18"
}'
```

* See how Mesos-slave will die :(

More details: http://www.mail-archive.com/dev@mesos.apache.org/msg33484.html

base:
  '*':
    - mesos-common
  'host:mesos-master':
    - match: grain
    - mesos-master
  'host:mesos-slave-*':
    - match: grain
    - mesos-slave

/etc/mesos-master/advertise_ip:
  file.managed:
    - user: root
    - group: root
    - mode: 644
    - contents: 192.168.255.10

master.packages:
  pkg.installed:
    - pkgs:
      - marathon
      - mesosphere-zookeeper

mesos-slave:
  service.dead:
    - enable: False
    - watch:
      - file: /etc/mesos-master/advertise_ip

mesos-master:
  service.running:
    - enable: True

marathon:
  service.running:
    - enable: True

zookeeper:
  service.running:
    - enable: True

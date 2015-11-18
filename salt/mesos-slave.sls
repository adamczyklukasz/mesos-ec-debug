python-pip:
  pkg.installed: []

python-devel:
  pkg.installed: []

six:
  pip.installed:
    - upgrade: True

pip-packages:
  pip.installed:
    - pkgs:
      - python-daemon
      - psutil
      - mesos.interface
    - require:
      - pkg: python-pip
      - pkg: python-devel
      - pip: six

mesos-master:
  service.dead:
    - enable: False

mesos-slave:
  service.running:
    - enable: True
    - watch:
      - file: /etc/mesos/zk
      - file: /etc/mesos-slave/ip
      - file: /etc/mesos-slave/hostname
      - file: /etc/mesos-slave/containerizers
      - file: /etc/mesos-slave/containerizer_path
      - pip: pip-packages

/etc/mesos/zk:
  file.managed:
    - user: root
    - group: root
    - mode: 644
    - contents: 192.168.255.10:5050

/etc/mesos-slave/ip:
  file.managed:
    - user: root
    - group: root
    - mode: 644
    - contents: {{ salt['grains.get']('ip4_interfaces:enp0s8', '') }}

/etc/mesos-slave/hostname:
  file.managed:
    - user: root
    - group: root
    - mode: 644
    - contents: {{ salt['grains.get']('ip4_interfaces:enp0s8', '') }}

/etc/mesos-slave/containerizers:
  file.managed:
    - user: root
    - group: root
    - mode: 644
    - contents: external

/etc/mesos-slave/containerizer_path:
  file.managed:
    - user: root
    - group: root
    - mode: 644
    - contents: /opt/ecp/ecp.py


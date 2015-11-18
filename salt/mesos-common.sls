base.packages:
  pkg.installed:
    - pkgs:
      - htop
      - vim-enhanced
      - screen
      - curl

/etc/yum.repos.d/mesosphere.repo:
  file.managed:
    - source: salt://mesos-common/mesosphere.repo
    - user: root
    - group: root
    - mode: 644

/etc/pki/rpm-gpg/RPM-GPG-KEY-mesosphere:
  file.managed:
    - source: salt://mesos-common/RPM-GPG-KEY-mesosphere
    - user: root
    - group: root
    - mode: 644

mesos:
  pkg.installed:
    - require:
      - file: /etc/pki/rpm-gpg/RPM-GPG-KEY-mesosphere
      - file: /etc/yum.repos.d/mesosphere.repo

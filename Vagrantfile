Vagrant.configure("2") do |config|
  mesos_slaves_quantity = 1
  config.vm.synced_folder "salt/", "/srv/salt/"
  config.vm.synced_folder "ecp/", "/opt/ecp/"

  config.vm.provision :salt do |salt|
    salt.run_highstate = true
#    salt.log_level = "warning"
    salt.masterless = true
  end

  config.vm.define "mesos-master" do |master|
    master.vm.box = "bechtoldt/centos-7.0-salt-2015.8.0"
    master.vm.hostname = "mesos-master"
    master.vm.network :private_network, ip: "192.168.255.10"
    master.vm.provider "virtualbox" do |v|
      v.memory = 512
      v.cpus = 1
    end
  end

  mesos_slaves_quantity.times do |i|
    config.vm.define "mesos-slave-#{i}" do |slave|
      slave.vm.box = "bechtoldt/centos-7.0-salt-2015.8.0"
      slave.vm.hostname = "mesos-slave-#{i}"
      slave.vm.network :private_network, ip: "192.168.255.#{100+i}"
      slave.vm.provider "virtualbox" do |v|
        v.memory = 1024
        v.cpus = 1
      end
    end
  end
end


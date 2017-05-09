Vagrant.configure("2") do |config|
  config.ssh.insert_key = false
  config.vm.box = "centos/7"
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "private_network", type: "dhcp"

  config.vm.synced_folder "./simpleapp", "/usr/local/python/simpleapp", type: "rsync",
	rsync__exclude: ".git/"

  config.vm.provision "shell", inline: <<-SHELL
    sudo rpm --import https://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-7
    sudo yum -y install epel-release
    sudo yum -y install ansible
  SHELL

  config.vm.provision "ansible" do |ansible|
    ansible.verbose = "v"
    ansible.playbook = "playbook.yaml"
  end
end

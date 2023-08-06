# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-22.04"
  config.vm.provider "virtualbox" do |v|
      v.memory = 2048
  end

  # provision
  config.vm.provision "shell" do |shell|
    shell.inline = "apt-get update"
  end
end

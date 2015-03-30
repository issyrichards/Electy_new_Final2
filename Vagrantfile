Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/trusty64"

  config.vm.define "cfg" do |cfg|
    cfg.vm.hostname = 'cfg'
    cfg.vm.network :private_network, ip: "33.33.33.42"
    cfg.vm.synced_folder "./", "/opt/cfg"
  end

end

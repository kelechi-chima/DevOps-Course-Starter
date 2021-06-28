Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"

  # The following lines will provision or set up the virtual machine by executing the referenced shell scripts.
  config.vm.provision "shell", privileged: false, path: "vagrant_scripts/install_pyenv_prerequisites.sh"
  config.vm.provision "shell", privileged: false, path: "vagrant_scripts/install_pyenv.sh"
  config.vm.provision "shell", privileged: false, path: "vagrant_scripts/configure_pyenv.sh"
  config.vm.provision "shell", privileged: false, path: "vagrant_scripts/install_python.sh"
  config.vm.provision "shell", privileged: false, path: "vagrant_scripts/install_poetry.sh"

  # The below will be triggered after 'vagrant up' completes.
  # It installs the app dependencies, then runs the app as a background process.
  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script"
    trigger.run_remote = {privileged: false, inline: "
      cd /vagrant
      poetry install
      nohup poetry run flask run --host=0.0.0.0 > logs.txt 2>&1 &
    "}
  end

  # Forward requests to port 5000 on the host machine to port 5000 on the guest machine.
  config.vm.network "forwarded_port", guest: 5000, host: 5000
end

#!/bin/bash

# Install prerequisite software
sudo apt-get -y update
sudo apt-get -y install build-essential vim git openjdk-7-jre openjdk-7-jdk curl wget python-pip sqlite3 zip
sudo apt-get -y build-dep python-psycopg2

# Setup Django
sudo pip install Django

# Add in python module prerequisites (they are not put into a 
# virtualenv since this is the only app that will run on the VM.)
sudo pip install -r /vagrant/requirements.txt

# Add a helpful message once a user logs in to the SSH shell.
sudo echo "\necho \"Run Videeo using the following command: \\\"python /vagrant/manage.py runserver [::]:8000\\\"\"" >> /home/vagrant/.bashrc

# Show message immediately after VM is built, telling user how to SSH into it.
echo "You may now ssh into this VM using the command 'vagrant ssh'"
#!/bin/bash

# Basic Setup
sudo apt-get -y update
sudo apt-get -y install build-essential vim git openjdk-7-jre openjdk-7-jdk curl wget python-pip sqlite3 zip
sudo apt-get -y build-dep python-psycopg2

# # Setup Java Play
# mkdir play
# cd play
# wget http://downloads.typesafe.com/play/2.1.4/play-2.1.4.zip
# unzip play-2.1.4.zip
# echo "PATH:$PATH:/$HOME/play/play-2.1.4/" >> ~/.bashrc

# Setup Django
sudo pip install Django
sudo pip install -r /vagrant/requirements.txt

# # Setup MySQL
# sudo apt-get -y install mysql-server

# # Setup Postgres
# sudo apt-get -y install postgresql postgresql-client pgadmin3


# # Setup Ruby on Rails
# sudo apt-get install rails
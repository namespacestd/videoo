Videeo
======

Videeo is a social movie browsing, reviewing and rating site.


To run in Vagrant
-----------------
1) Install vagrant on your machine
2) Open a terminal and navigate into the source code root folder
3) Start the Vagrant VM...
	vagrant up
4) SSH into the Vagrant VM...
	vagrant ssh
5) Start the Django development server...
	python /vagrant/manage.py runserver [::]:8000
6) The site can be viewed by going to the following URL on the host machine:
	http://localhost:8000

Some test data will automatically be populated in the application.  The following user is automatically set up as an initial admin:
	User: ase1
	Password: password123


To run outside of Vagrant
-------------------------
1) Install python and django on your machine
2) Install PIP, and prerequisites using: 'pip install -r requirements.txt'
3) Enter your TMDB API key into the file '/movie/settings.py'
4) Start the site using 'python manage.py runserver'

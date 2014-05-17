#! /bin/sh
sudo su

# pull from github
git pull origin master

# deploy apache configuration
cp ./config/default /etc/apache2/sites-available/
service apache2 restart

# return to user
exit
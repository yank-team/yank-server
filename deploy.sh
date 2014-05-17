#! /bin/sh

# pull from github
echo "pulling from repo"
git pull origin master

# deploy apache configuration
echo "update apache config"
sudo cp ./config/default /etc/apache2/sites-available/
sudo service apache2 restart

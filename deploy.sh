#! /bin/sh

# pull from github
echo "pulling from repo"
git pull origin $1

# deploy apache configuration
echo "update apache config"
sudo cp ./config/default /etc/apache2/sites-available/
sudo service apache2 restart

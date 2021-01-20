#!/bin/bash

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

# cleanup web drivers folder
rm -r $parent_path/cache/drivers
mkdir $parent_path/cache/drivers
mkdir $parent_path/logs

sudo apt-get install unzip
echo "Successfully installed unzip dpkg"
sudo apt-get install pipenv
echo "Successfully installed pipenv dpkg"

# download web drivers
echo "Downloading Chrome web_driver for Selenium automation package ..."
wget https://chromedriver.storage.googleapis.com/88.0.4324.27/chromedriver_linux64.zip -P $parent_path/cache/drivers

echo "Downloading Firefox web_driver for Selenium automation package ..."
wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz -P $parent_path/cache/drivers

# unzip web drivers
unzip -q $parent_path/cache/drivers/chromedriver_linux64.zip -d $parent_path/cache/drivers 
tar -xvzf $parent_path/cache/drivers/geckodriver-v0.29.0-linux64.tar.gz -C $parent_path/cache/drivers 

# cleanup and setup python virtual env
pipenv --rm
pipenv install --skip-lock

echo "IMPORTANT!!!! Heavy file download approximately near 2GB. Please use proper internet connection!!!!"
read -p "Are you sure you want to continue? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    pipenv run python dictionary_downloader.py
fi

chmod +x run_server.sh

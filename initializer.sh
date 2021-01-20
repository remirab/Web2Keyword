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

GECKO_DRIVER_VERSION='v0.29.0'
wget https://github.com/mozilla/geckodriver/releases/download/$GECKO_DRIVER_VERSION/geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz
tar -xvzf geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz -C $parent_path/cache/drivers
rm geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz
chmod +x $parent_path/cache/drivers/geckodriver
sudo cp $parent_path/cache/drivers/geckodriver /usr/bin/
echo "browser_driver_path="\"/usr/bin/geckodriver"\"" > $parent_path/driver.ini

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

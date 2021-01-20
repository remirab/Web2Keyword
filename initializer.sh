#!/bin/bash

echo "$(whoami)"
[ "$UID" -eq 0 ] || exec sudo "$0" "$@"

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

# cleanup web drivers folder
rm -r $parent_path/cache
mkdir $parent_path/cache
mkdir $parent_path/cache/drivers

# check install unzip dpkg
if dpkg --get-selections | grep "unzip[[:space:]]*install$" >/dev/null
    then
        if apt-get install unzip >/dev/null
            then
            echo "Successfully installed unzip dpkg"
        fi
fi

# check install pipenv dpkg
if dpkg --get-selections | grep "pipenv[[:space:]]*install$" >/dev/null
    then
        if apt-get install pipenv 
            then
            echo "Successfully installed pipenv dpkg"
        fi
fi

echo "Downloading Chrome web_driver for Selenium automation package ..."
wget https://chromedriver.storage.googleapis.com/88.0.4324.27/chromedriver_linux64.zip -P $parent_path/cache/drivers

echo "Downloading Firefox web_driver for Selenium automation package ..."
wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz -P $parent_path/cache/drivers

unzip -q $parent_path/cache/drivers/chromedriver_linux64.zip -d $parent_path/cache/drivers 
tar -xvzf $parent_path/cache/drivers/geckodriver-v0.29.0-linux64.tar.gz -C $parent_path/cache/drivers 

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
#!/bin/bash

urls=`cat ./download.html | \grep xls`

while read line
do
    link=$(echo $line | cut -d'"' -f2)
    name=$(echo $line | sed 's/<a .*>\(.*\)<\/a>.*/\1/' | tr -d '[:blank:]')
    echo -n "Downloading $name ..."
    curl -s "$link" > ./data/$name
    echo " Done!"
done <<< "$urls";

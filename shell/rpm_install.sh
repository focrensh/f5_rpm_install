#!/bin/bash

user="admin"
pass="admin"
port="8443"
rpm="../rpms/f5-appsvcs-3.8.0-3.noarch.rpm"

while read bigip; do
  echo "#################################"
  echo "Starting------- $bigip"
  echo "#################################"
  echo -n "{\"HOST\": \"$bigip\",\"USER\": \"$user\", \"PASS\": \"$pass\", \"PORT\": \"$port\"}" > devconfig.json
  icrdk deploy $rpm
done <bigips.txt

rm devconfig.json -f
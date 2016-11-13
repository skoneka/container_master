#!/bin/sh
#run after reboot
rm -r /var/lib/origin
systemctl restart docker.service; oc cluster up
oc cluster up
docker rm $(docker ps -a -q)

echo Now reboot

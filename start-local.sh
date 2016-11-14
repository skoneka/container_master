#!/bin/sh

cat << EOF
#startmeup:
# reboot
#
rsync -avx --delete /media/a/355fc64b-d7c7-4a25-9d43-ffa8fdf9275f/hipopotam/home/a/Dropbox_skoneka/Dropbox/master/measure-images root@docker2:~/

systemctl restart docker.service; oc cluster up
time oc new-app https://github.com/skoneka/container_testme.git --name "testme-image"
#oc start-build testme-image --from-dir=/root/measure-images/container_testme
oc logs -f bc/testme-image|grep 5000

oc scale --replicas=0 dc/testme-image

rsync -avx --delete /media/a/355fc64b-d7c7-4a25-9d43-ffa8fdf9275f/hipopotam/home/a/Dropbox_skoneka/Dropbox/master/measure-images root@docker2:~/

cd /root/measure-images/container_master
bash /root/measure-images/container_master/start-local.sh /root/logs/master.log
curl '159.100.252.59:8080/timestamp?comment=START' && curl '159.100.252.59:8080/container_next?count=1&comment="first+container"'
EOF


DOCKER_REPO_URL=$(oc logs -f bc/testme-image |grep :5000|cut -d' ' -f3)
ENGINE="$1"
LOGFILE="$2"
sed -i "s#DOCKER_REPO_URL=.*#DOCKER_REPO_URL=\"$DOCKER_REPO_URL\"#" wsgi.py
sed -i "s#LOGFILE=.*#LOGFILE=\"$LOGFILE\"#" wsgi.py
sed -i "s#ENGINE=.*#ENGINE=\"$ENGINE\"#" wsgi.py
exec gunicorn -c config.py wsgi -b :8080 --access-logfile -

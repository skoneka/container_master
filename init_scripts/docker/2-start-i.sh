LOG=/root/logs/docker-`date +%s`.log 
cd /root/measure-images/container_master
cat /proc/meminfo /proc/cpuinfo > $LOG
ps auxww >> $LOG
bash start-local.sh docker $LOG.container 
#sleep 3;
cat <<EOF
Now run
curl '159.100.252.59:8080/timestamp?comment=START' && curl '159.100.252.59:8080/container_next?count=1&comment="first+container"'
EOF

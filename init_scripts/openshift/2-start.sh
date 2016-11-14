
LOG=/root/logs/openshift-`date +%s`.log 
cd /root/measure-images/container_master
cat /proc/meminfo /proc/cpuinfo > $LOG
ps auxww >> $LOG
nohup bash start-local.sh openshift $LOG.container 2>&1 >> $LOG &
sleep 3;
curl '159.100.252.59:8080/timestamp?comment=START' && curl '159.100.252.59:8080/container_next?count=1&comment="first+container"'

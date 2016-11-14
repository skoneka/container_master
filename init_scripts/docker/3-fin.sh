curl '159.100.252.59:8080/timestamp?comment=FIN'
LFILE=/root/logs/`ls -rt1 /root/logs|tail -1`.fin
docker ps 2>&1 >> $LFILE
cat /proc/meminfo /proc/cpuinfo >> $LOG
ps auxww >> $LOG

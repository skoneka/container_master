curl '159.100.252.59:8080/timestamp?comment=FIN'
LFILE=/root/logs/`ls -rt1 /root/logs|tail -1`
cat /proc/meminfo /proc/cpuinfo >> $LFILE.fin
ps auxww >> $LFILE.fin
cat /var/log/messages > $LFILE.messages
docker ps 2>&1 >> $LFILE.fin

curl '159.100.252.59:8080/timestamp?comment=FIN'
LFILE=/root/logs/`ls -rt1 /root/logs|tail -1`
docker ps 2>&1 >> $LFILE.fin
oc status -v 2>&1 >> $LFILE.fin
oc login -u system:admin
oc describe nodes 2>&1 >> $LFILE.fin
docker logs origin 2>&1 |tee $LFILE.origin > /dev/null
cat /var/log/messages > $LFILE.messages


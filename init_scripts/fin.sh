curl '159.100.252.59:8080/timestamp?comment=FIN'
LFILE=/root/logs/`ls -rt1 /root/logs|tail -1`.fin
docker ps 2>&1 >> $LFILE
oc status -v 2>&1 >> $LFILE
oc login -u system:admin
oc describe nodes 2>&1 >> $LFILE
docker logs origin 2>&1 |tee $LFILE.origin > /dev/null



systemctl restart docker.service; oc cluster up
cat >> /var/lib/origin/openshift.local.config/node-159.100.252.59/node-config.yaml <<EOF
kubeletArguments:
  max-pods:
  - "100000"
EOF
docker restart origin
sleep 10;
time oc new-app https://github.com/skoneka/container_testme.git --name "testme-image"
#oc start-build testme-image --from-dir=/root/measure-images/container_testme
echo Now run
echo "oc logs -f bc/testme-image|grep 5000"
echo oc scale --replicas=0 dc/testme-image

from __future__ import print_function
from flask import Flask, request
from time import time
from subprocess import Popen
from os import getloadavg
from myutil import get_meminfo

#startmeup:
# rsync -avx --delete /media/a/355fc64b-d7c7-4a25-9d43-ffa8fdf9275f/hipopotam/home/a/Dropbox_skoneka/Dropbox/master/measure-images root@docker2:~/
# cd measure-images/container_master
# bash start-local.sh
# systemctl restart docker.service; oc cluster up
# time oc new-app https://github.com/skoneka/container_testme.git --name "testme-image"
# oc scale --replicas=0 dc/testme-image
# curl '159.100.252.59:8080/timestamp?comment=START' && curl '159.100.252.59:8080/container_next?count=1&comment="first+container"'



DOCKER_REPO_URL="172.30.18.89:5000/myproject/testme-image:latest"
MEM_RAM_THRESHOLD=2900000

application = Flask(__name__)
flog = open ("/tmp/containerup.log", "a")

FLAG_ABORT=False



def get_status(comment):
    global FLAG_ABORT
    #format containerIP,epoch_timestamp, usedram, 1min_cpu_load_average comment
    epoch_time = time()
    container = request.remote_addr
    mem_ram = get_meminfo()['MemAvailable']
    load = getloadavg()[0]
    if mem_ram <= MEM_RAM_THRESHOLD:
        FLAG_ABORT=True
    return "%s,%f,%d,%g,%s" % (container,epoch_time,mem_ram,load,comment)


@application.route("/timestamp", methods=['GET'])
def url_timestamp():
    status = get_status("timestamp " + request.args.get('comment'))
    print(status, file=flog); flog.flush()
    return status, 200


@application.route("/container_next", methods=['GET'])
def url_container_next():
    status = get_status("container_next " + request.args.get('comment'))
    
    if FLAG_ABORT:
        status = status + " ABORT(MEM_RAM_THRESHOLD)"
        print(status, file=flog); flog.flush()
        return status, 417
    else:
        count = int(request.args.get('count'))
        Popen("""time oc new-app "%s" --name "testme-%d" --insecure-registry""" % (DOCKER_REPO_URL, count), shell=True).wait()
        return status, 201


    

#@application.route("/", methods=['GET'])
#def url_test():
#    print(request.args)
#    return "test",200


  
#@application.route("/container_start", methods=['GET'])
#def url_container_start():  
#    count = int(request.args.get('count'))
#    Popen("""time oc new-app "%s" --name "testme-%d" --insecure-registry""" % (DOCKER_REPO_URL, count), shell=True).wait()
#    
#    return "container_start", 200

# print available cluster memory here too
# should container get their startup time to get delays for  single containers? or just use simple scale to time different numbers of containers being created at once

# 

if __name__ == "__main__":
    application.run()

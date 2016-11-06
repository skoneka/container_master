from __future__ import print_function
from flask import Flask, request
from time import time
from subprocess import Popen
from os import getloadavg
from myutil import get_meminfo





DOCKER_REPO_URL="REPLACEME_DOCKER_REPO_URL"
MEM_RAM_THRESHOLD=100000

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
        print(status, file=flog); flog.flush()
        count = int(request.args.get('count'))
        Popen("""time oc new-app "%s" --name "testme-%d" --insecure-registry""" % (DOCKER_REPO_URL, count), shell=True).wait()
        return status, 201


    

#@application.route("/", methods=['GET'])
#def url_test():
#    print(request.args)
#    return "test",200

if __name__ == "__main__":
    application.run()

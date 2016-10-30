from __future__ import print_function
from flask import Flask, request
from time import time
from myutil import get_meminfo
application = Flask(__name__)
flog = open ("/tmp/containerup.log", "a")

@application.route("/timestamp")
def url_timestamp():
    epoch_time = time()
    mem_ram = get_meminfo()['MemAvailable']
    status = "0,%f,%d" % (epoch_time,mem_ram)
    #status = "TIMESTAMP %f" % (epoch_time)
    print(status, file=flog); flog.flush()
    return status

@application.route("/")
@application.route("/container_up")
def url_container_up():
    epoch_time = time()
    container = request.remote_addr
    mem_ram = get_meminfo()['MemAvailable']
    #format containerIP,timestamp,usedram
    status = "%s,%f,%d" % (container, epoch_time, mem_ram)
    #status = "container %s timestamp %f" % (container, epoch_time)
    print(status, file=flog); flog.flush()
    return status
# print available cluster memory here too
# should container get their startup time to get delays for  single containers? or just use simple scale to time different numbers of containers being created at once

# 

if __name__ == "__main__":
    application.run()

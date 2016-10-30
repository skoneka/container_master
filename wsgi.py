from flask import Flask, request
from time import time
application = Flask(__name__)

@application.route("/timestamp")
def url_timestamp():
    epoch_time = time()
    status = "TIMESTAMP %f" % (epoch_time)
    print (status)
    return status

@application.route("/")
@application.route("/container_up")
def url_container_up():
    epoch_time = time()
    container = request.remote_addr
    status = "container %s timestamp %f" % (container, epoch_time)
    print (status)
    return status
# print available cluster memory here too
# should container get their startup time to get delays for  single containers? or just use simple scale to time different numbers of containers being created at once

# 

if __name__ == "__main__":
    application.run()

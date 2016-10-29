from flask import Flask, request
from time import time
application = Flask(__name__)

@application.route("/")
def container_up():
    epoch_time = time()
    container = request.remote_addr
    status = "container %s timestamp %f" % (container, epoch_time)
    print (status)
    return status

if __name__ == "__main__":
    application.run()

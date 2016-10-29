from flask import Flask, request
application = Flask(__name__)

@application.route("/")
def container_up():
    container = request.args['container']
    time = request.args['time']
    return "container %s timestamp %s" % (container, time)

if __name__ == "__main__":
    application.run()

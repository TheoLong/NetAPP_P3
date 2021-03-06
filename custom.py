from flask import Flask, request, Response, make_response
import socket
from zeroconf import ServiceInfo, Zeroconf
from subprocess import check_output
import json
t1 = "Hello1"
t2 = "Hello2"

'''
==================  zeroconf  ====================
'''
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('www.google.com', 0))
ipAddress = s.getsockname()[0]
desc = {'path': '/~paulsm/'}
info = ServiceInfo("_http._tcp.local.",
                       "Custom._http._tcp.local.",
                       socket.inet_aton(ipAddress), 8082, 0, 0,
                       desc, "ash-2.local.")

zeroconf = Zeroconf()
print("Registration of a service " +str(ipAddress))
zeroconf.register_service(info)

'''
==================  flask  ====================
'''
app = Flask(__name__)

@app.route('/t1_update', strict_slashes=True, methods=['POST'])
def update_t1():
    text1 = request.get_data()
    global t1
    t1 = text1
    return "update success!"

@app.route('/t2_update', strict_slashes=True, methods=['POST'])
def update_t2():
    text2 = request.get_data()
    global t2
    t2 = text2
    return "update success!"

@app.route('/t1', strict_slashes=True, methods=['GET'])
def get_t1():
    return t1

@app.route('/t2', strict_slashes=True, methods=['GET'])
def get_t2():
    return t2

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082, debug=True)

print("Unregistering...")
zeroconf.unregister_service(info)
zeroconf.close()

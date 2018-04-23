import canvas_token as token
import requests
import codecs
from flask import Flask, request, Response, make_response, send_file
from functools import wraps
from pymongo import MongoClient
import io
import json
import pickle
import socket
import sys
import collections
from time import sleep
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf
'''
==================  zeroconf  ====================
'''
LED_ip = ''
custom_ip = ''
def on_service_state_change(zeroconf, service_type, name, state_change):
    global LED_ip
    global custom_ip
    if name == "LED._http._tcp.local." and LED_ip == '':
        if state_change is ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            if info:
                LED_ip = str("%s:%d" % (socket.inet_ntoa(info.address), info.port))
                print ("Got LED ip: " + LED_ip)
    elif name == "Custom._http._tcp.local." and custom_ip == '':
        if state_change is ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            if info:
                custom_ip = str("%s:%d" % (socket.inet_ntoa(info.address), info.port))
                print ("Got custom ip: " + custom_ip)

zeroconf = Zeroconf()
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", handlers=[on_service_state_change])
print ("==============  Waiting for Custom and LED ip")
while LED_ip == '' or custom_ip =='':
    sleep(0.1)
zeroconf.close()


led_addr = 'http://'+LED_ip
custom_addr = 'http://'custom_ip
#--------------set up flask--------------
app = Flask(__name__)
#--------------connect to mongodb server-------------
client = MongoClient('localhost', 27017)
db = client.canvas
post = db.posts


def upload(file_name,file):
    #------------step1---get authon and get upload url--------------
    auth = 'Bearer '+token.canvas_token
    headers = {
    'Authorization': auth,
    }
    files = {
    'name': (None, file_name),
    'parent_folder_path': (None,'/')
    }
    response = requests.post('https://canvas.vt.edu/api/v1/groups/52716/files', headers=headers, files=files)
    response = response.json()
    #----------step2---send back parameters with file to url--------
    url = response["upload_url"]
    parameter = collections.OrderedDict(response["upload_params"])
    parameter['file'] = file
    response = requests.post(url, files=parameter)
    #----------step3---error handling-----------------------------
    print(response.status_code)
    print(response.text)
    if response.status_code != 200:
        return "error upload unsuccess"
    else:
        return "upload success"

#list all the file in group root folder, list the file in a dic
def list_file():
    auth = 'Bearer '+token.canvas_token
    headers = {
    'Authorization': auth,
    }
    response = requests.get('https://canvas.vt.edu/api/v1/groups/52716/files/', headers=headers)
    response = response.json()
    #print (response)
    dic = {}
    for file in response:
        if file['folder_id'] == 1057446:
            dic[file['filename']] = file['url']
    return dic

def download_file(url):
    auth = 'Bearer '+token.canvas_token
    headers = {
    'Authorization': auth,
    }
    response = requests.get(url, headers=headers)
    return response.content

# 3 function below is open source code obtain from
#---------------------http://flask.pocoo.org/snippets/8/, posted by Armin Ronacher
def check_auth(username, password):
    result = post.find_one({'username': username, 'password':password})
    return result != None

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response('Could not verify your access level for that URL.\n' 'You have to login with proper credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
#--------------------------------web sever-------------------------------

#list files
@app.route('/canvas')
@requires_auth
def canvas():
    s = ""
    dic = list_file()
    #print (dic)
    for key in dic:
        s = s + " " + key
    return s

#upload files
# test using curl curl -X POST -u yunfei:guoyunfei -F "file=@/Users/YunfeiGuo/Desktop/test.txt" "http://localhost:8081/canvas/upload/test.txt"
@app.route('/canvas/upload/<filename>', strict_slashes=True, methods=['POST'])
@requires_auth
def canvas_upload(filename):
    f = request.files['file']
    #print(f)
    return upload(filename,f)

#download files
@app.route('/canvas/download/<filename>', strict_slashes=True, methods=['GET'])
@requires_auth
def canvas_download(filename):
    dic = list_file()
    f = download_file(dic[filename])
    return send_file( io.BytesIO(f), as_attachment=True, attachment_filename= filename)

@app.route('/led', strict_slashes=True, methods=['POST'])
@requires_auth
def led_set_color():
    #set led color
    red = request.form['red']
    green = request.form['green']
    blue = request.form['blue']
    rate = request.form['rate']
    state = request.form['state']
    dic = {'red':red, 'green':green, 'blue':blue, 'rate':rate, 'state':state}
    response = requests.post(led_addr+'/led', data = dic)
    return response.text

@app.route('/led', strict_slashes=True, methods=['GET'])
@requires_auth
def led_status():
    #get led color
    response = requests.get(led_addr+'/led')
    return response.text

@app.route('/t1_update', strict_slashes=True, methods=['POST'])
@requires_auth
def send_text1():
    #send text1
    text1 = request.form['text']
    response = requests.post(custom_addr+'/t1_update', data = text1)
    return response.text

@app.route('/t2_update', strict_slashes=True, methods=['POST'])
@requires_auth
def send_text2():
    #send text2
    text2 = request.form['text']
    response = requests.post(custom_addr+'/t2_update', data = text2)
    return response.text

@app.route('/t1', strict_slashes=True, methods=['GET'])
@requires_auth
def get_text1():
    #get text1
    response = requests.get(custom_addr+'/t1')
    return response.text

@app.route('/t2', strict_slashes=True, methods=['GET'])
@requires_auth
def get_text2():
    #get text2
    response = requests.get(custom_addr+'/t2')
    return response.text

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)

import canvas_token as token
import requests
import codecs
from flask import Flask, request, Response, make_response, send_file
from functools import wraps
from pymongo import MongoClient
import io
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
    parameter = response["upload_params"]
    parameter['file'] = (file_name, file)
    response = requests.post(url, files=parameter)
    #----------step3---error handling-----------------------------
    if response.status_code != 200:
        return "error: upload unsuccess"
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

#---------------------- code below is open source code obtain from
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
# test using curl curl -X POST -u yunfei:guoyunfei -F "data=@/Users/YunfeiGuo/Desktop/test.txt" "http://localhost:8081/canvas/upload/test.txt"

@app.route('/canvas/upload/<filename>', strict_slashes=True, methods=['POST'])
@requires_auth
def canvas_upload(filename):
    f = request.get_data()
    return upload(filename,f)

#download files
@app.route('/canvas/download/<filename>', strict_slashes=True, methods=['GET'])
@requires_auth
def canvas_download(filename):
    dic = list_file()
    f = download_file(dic[filename])
    return send_file( io.BytesIO(f), as_attachment=True, attachment_filename= filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)

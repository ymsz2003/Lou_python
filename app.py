from flask import Flask,render_template,abort
import json
import os
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
path = '/home/shiyanlou/files'
files = os.listdir(path)
text = []
for file in files:
    if os.path.splitext(file)[1] == '.json':
        with open (path+'/'+file,'r') as load_f:
            load_dict = json.load(load_f)
            load_dict.update({'filename':os.path.splitext(file)[0]})
            text.append(load_dict)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
@app.route('/')
def index():
    text
    return render_template('index.html', text=text)
@app.route('/files/<filename>')
def file_index(filename):
    flag = False
    for file in text:
        if filename == file['filename']:
            flag = True
    if flag == False:
        abort(404)
    return render_template('file.html', filename = filename, text = text)



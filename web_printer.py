import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from subprocess import run


UPLOAD_FOLDER = 'FILE_STORE'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def printFile(file,pages,orientation):
    command = ['lpr',file]
    if pages:
        command.extend(['-o',f'page-ranges={pages}'])
    if orientation=='Landscape':
        command.extend(['-o','orientation-requested=4'])
    print(command)
    ret = run(command)
    return ret.returncode






@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            # print(request.form,request.files)
            file = request.files.get('file',None)
            pages = request.form.get('pages')
            ornt  = request.form.get('orientation')
            if not file or file.filename == '':
                return render_template('out.html',data="No file attached")
            filename = secure_filename(file.filename)
            newpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(newpath)
            ret = printFile(newpath,pages,ornt)

            if ret==0:
                txt = "Print job submitted successfully"
            else:
                txt = "Unable to submit print job"
        except Exception as e:
            print(e)
            txt = "Unable to submit print job"

        return render_template('out.html',data=txt)

    return render_template('index.html')


if __name__ == '__main__':
    # from waitress import serve
    # serve(app,host='0.0.0.0',port=8080)
    app.run(host='0.0.0.0', port=8080,debug=True)


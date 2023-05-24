import os
import logging
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from subprocess import run
from datetime import datetime
import subprocess

UPLOAD_FOLDER = 'FILE_STORE'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def makeLogger(logFile):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logFile)
    logger.addHandler(fh)
    return logger


logger = makeLogger('webprinter.log')
def getNumberOfPage(pdfFile):
    t = subprocess.run(f"pdfinfo {pdfFile}  | awk '/^Pages:/ {{print $2}}'",shell=True,stdout=subprocess.PIPE)#,text=True)
    return t.stdout.strip()

# check the list of available printers with `lpstat -p -d` 
# pass the particular printer with `-P` flag to `lpr`


def printFile(file,pages,orientation,per_page):
    # return 0
    command = ['lpr',file,'-o', 'fit-to-page', '-o', f'number-up={per_page}', '-P', 'HP-ColorLaserJet-M153-M154']
    #^ Auto fit to page, provide custom scale later
    pg = getNumberOfPage(file)
    if pages:
        command.extend(['-o',f'page-ranges={pages}'])
    if orientation=='Landscape':
        command.extend(['-o','orientation-requested=4'])
    ret = run(command)
    logger.info(f"[{datetime.now().strftime('%I:%M:%S %p %d-%m-%Y')}] - File: {file}, Total No. of pages: {pg}, Pagesto print: {pages}, Per-page: {per_page}")
    #^ streamline this logic
    return ret.returncode





@app.route('/', methods=['GET', 'POST'])
def upload_file():
    retCodes = []
    if request.method == 'POST':
        try:
            pages = request.form.get('pages')
            ornt  = request.form.get('orientation')
            per_page = request.form.get('perpage')
            for file in request.files.getlist('file'):

                if not file or file.filename == '':
                    return render_template('out.html',data="No file attached")
                filename = secure_filename(file.filename)
                newpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                file.save(newpath)
                print(newpath)
            
                ret = printFile(newpath,pages,ornt,per_page)
                retCodes.append(ret)

            if all(retCodes)==0:
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
    # gunicorn -w 4 'web_printer:app' -b '0.0.0.0:8080'
    app.run(host='0.0.0.0', port=8080,debug=True)


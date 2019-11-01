import os
import zipfile
from flask import Flask, request, send_from_directory, send_file, Response
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/popashka/easy/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024 * 1024


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and (file.content_type.rsplit('/', 1)[1] in ALLOWED_EXTENSIONS).__bool__():
            filename = secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER'] + filename)
            pat = UPLOAD_FOLDER + filename
            filename = pat
            with zipfile.ZipFile('/home/popashka/d.zip', 'a') as myzip:
                myzip.write(pat, filename)
            res =  send_file('/home/popashka/d.zip',
                            mimetype='application/octet-stream',
                            as_attachment=True,
                            attachment_filename='d.zip')
            myzip.close()
            os.remove('/home/popashka/d.zip')
            return res



    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



if __name__ == '__main__':
    app.run(debug=True)

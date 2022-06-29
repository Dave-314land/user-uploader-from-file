import os
import pandas
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename


PATH = os.getcwd()
PROCESSING_DIR = "processing"
PROCESSING_DIR_FILE_PATH = PATH + "\\" + PROCESSING_DIR + "\\"


app = Flask(__name__)
CONFIG_FILE = 'config_vars.py'
app.config.from_pyfile(CONFIG_FILE)


@app.route("/success")
def success_message():
    return "<p>Success!</p>"


@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('success_message', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if (__name__ == "__main__"):
    app.run(port = 5000)

    # Find all uploaded csv files
    csv_files = [file for file in os.listdir(PROCESSING_DIR_FILE_PATH) if file.endswith('.csv')]

    # Import the csv file(s) into pandas data frame(s)
    user_df_dict = {}
    for file in csv_files:
        try:
            user_df_dict[file] = pandas.read_csv(PROCESSING_DIR_FILE_PATH + file)
        except UnicodeDecodeError:
            user_df_dict[file] = pandas.read_csv(PROCESSING_DIR_FILE_PATH + file, encoding="ISO-8859-1")

    print(user_df_dict)
from flask import Flask, render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename
import os
import sqlite3

UPLOAD_FOLDER = os.getcwd() + '/databases'
ALLOWED_EXTENSIONS = {'db'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if (os.path.exists(os.getcwd() + '/databases' + filename)):
                os.remove(os.getcwd() + '/databases' + filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'file in system;)'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Загрузить базу данных Вашего университета</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Загрузить>
    </form> 
    '''


@app.route('/yargu', methods=['GET'])
def create_article():
    if request.method == "GET":
        conn = sqlite3.connect(os.getcwd() + '/databases/yargu.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM StudentsTable")
        result = cursor.fetchall()
        rlist = []
        for i in range(len(result)):
            rlist.append({
                "student_id": result[i][0],
                "fio": result[i][1],
                "university_name": result[i][2],
                "card_num": result[i][3],
                "stud_num": result[i][4],
                "marks": result[i][5],
                "achievements": result[i][6]})
        return str(rlist)


app.run(debug=False)